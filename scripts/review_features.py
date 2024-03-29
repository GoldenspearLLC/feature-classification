import streamlit as st

from db_selection import DBSelector


ACCEPT_FILE = '/home/imas/'
DISCARD_FILE = '/home/imas/'
PKL_PATH = '/home/imas/products.pkl'


def rerun():
    """
    Necessary to run streamlit tool
    """
    raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))


@st.cache(allow_output_mutation=True)
def get_db_selector():
    """
    Loads DB selector object
    :return: (DBSelector) object to retrieve and handle products from
    """
    return DBSelector(ACCEPT_FILE, DISCARD_FILE, save_products=True, pkl_path=PKL_PATH)


if __name__ == '__main__':

    db_selector = get_db_selector()

    if not hasattr(st.session_state, 'product_retriever'):
        st.session_state.product_retriever = db_selector.product_retriever()

    st.subheader('Feature tagging review tool')

    st.session_state.ctr = 0

    if st.session_state.ctr < db_selector.get_product_length():

        prod_show = next(st.session_state.product_retriever)

        img_url = prod_show['prevImage']['url']
        features = prod_show['productDescription']['features']

        feature_md = ''

        col1, col2 = st.beta_columns((1, 1))

        col1.image('/fileserver1/webdata' + img_url)

        for feature in features:
            if db_selector.feat_name_from_id(feature['featId']) not in ('NONE', 'UNKNOWN'):
                col2.write(db_selector.feat_name_from_id(feature['featId']))

        accept = col2.button('Accept')
        discard = col2.button('Discard')
        skip = col2.button('Skip')
        if accept:
            db_selector.accept_product(prod_show)
            st.session_state.ctr += 1
        if discard:
            db_selector.discard_product(prod_show)
            st.session_state.ctr += 1
        if skip:
            st.session_state.ctr += 1
