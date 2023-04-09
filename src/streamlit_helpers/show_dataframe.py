#!/usr/bin/python3.8
"""Open site showing pandas dataframe and charts for its every int column.

Usage:
$ streamlit run show_dataframe.py -- -d stats.csv
Runs a server which you can connect to via internet browser and IP adderss given by the server.
"""

import os
import sys
import argparse
# import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


def parseargs():
    """Parse arguments."""
    print('sys.argv: ')
    print(' '.join(sys.argv))
    print('--------------------------------------')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--dataframe", type=str, default=None,
        help="Input dataframe to show.")
    return parser.parse_args()


def plot_chart(df: pd.DataFrame, column: str):
    fig, ax = plt.subplots()
    ax.hist(df[column], bins=20)
    ax.set_title(column)
    st.pyplot(fig)

def print_charts(df: pd.DataFrame):

    int_columns = [column for column in df.columns if df[column].dtype == 'int64']

    for i in range(len(int_columns) // 2):
        col1, col2 = st.columns(2)
        with col1:
            if (i * 2) >= len(int_columns):
                break
            column = int_columns[i * 2]
            plot_chart(df, column)
            
        with col2:
            if (i * 2 + 1) >= len(int_columns):
                break
            column = int_columns[i * 2 + 1]
            plot_chart(df, column)

    for col in df.columns:
        st.write(col)
        st.write(df[col].dtype)


def main():
    """Main function for simple testing"""
    args = parseargs()

    st.set_page_config(page_title='DataFrame visualizer', layout='wide')

    if not args.dataframe:
        st.write("# Upload dataframe and enjoy.")

        df = None
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        print(f'uploaded_file: {uploaded_file}')

        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.write(df)
    else:
        if not os.path.exists(args.dataframe) or not os.path.isfile(args.dataframe):
            st.error("File you've passed as a dataframe does not exist.")
        else:
            st.write('# Enjoy your dataframe...')
            df = pd.read_csv(args.dataframe)
            st.write(df)
            print_charts(df)


if __name__ == "__main__":
    main()