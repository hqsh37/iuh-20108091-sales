
from cProfile import label
from importlib.resources import path
from os import link
from statistics import mode
from telnetlib import LINEMODE
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import dash_bootstrap_components as dbc
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

 # TẢI DỮ LIỆU TỪ FIRESTORE
cred = credentials.Certificate("./iuh-20108091-firebase-adminsdk-64kp5-5bba4304e2.json")
appLoadData = firebase_admin.initialize_app(cred)

dbFireStore = firestore.client()

queryResults = list(dbFireStore.collection(u'tbl20113031').where(u'DEALSIZE', u'==', 'Large').stream())
listQueryResult = list(map(lambda x: x.to_dict(), queryResults))

df = pd.DataFrame(listQueryResult)

df["YEAR_ID"] = df["YEAR_ID"].astype("str")#convert to string
df["QTR_ID"] = df["QTR_ID"].astype("str")
df = pd.read_csv('orginal_sales_data_edit.csv')
df.dropna()   



# DỮ LIỆU NHẬP CỨNG


figDoanhSoTheoNam = px.bar(df, x="YEAR_ID", y="SALES",  title='DOANH SỐ BÁN HÀNG THEO NĂM', color='SALES',
labels={'YEAR_ID':'Năm',  'SALES':'DOANH SỐ'})


figTiLeDongGopDanhSoTheoTungDoanhMuc = px.sunburst(df, path=['YEAR_ID', 'CATEGORY'], values='SALES',
color='QUANTITYORDERED',
labels={'parent':'Năm', 'labels':'Quý','QUANTITYORDERED':'Số lượng sản phẩm'},
title='TỈ LỆ ĐÓNG GÓP CỦA DOANH SỐ THEO TỪNG DANH MỤC TRONG TỪNG NĂM')



# Dữ liệu truy vấn 
tongDoanhSo = df['SALES'].sum().round(2)
doanhSoCaoNhat = df['SALES'].max().round(2)

#Tinh loi nhuan
#1 Tính total sale
df['TOTAL_SALES'] = df['QUANTITYORDERED'] * df['PRICEEACH']
#2 Tính lợi nhuận
df['Profit'] = (df['SALES'] - df['TOTAL_SALES']).round(2)
tongLoiNhuan = df['Profit'].sum().round(2)
loiNhuanCaoNhat = df['Profit'].max().round(2)

figTiLeDongGopLoiNhanTheoTungDoanhMuc = px.sunburst(df, path=['YEAR_ID', 'CATEGORY'], values='Profit',
color='Profit',
labels={'parent':'Năm', 'labels':'Quý','QUANTITYORDERED':'Số lượng sản phẩm'},
title='TỈ LỆ ĐÓNG GÓP CỦA LỢI NHUẬN THEO MỤC TRONG NĂM')


figLoiNhanTheoNam = px.line(data_frame=df, x="YEAR_ID", y="Profit",  title='LỢI NHUẬN BÁN HÀNG THEO NĂM', color='Profit',
labels={'YEAR_ID':'NĂM',  'Profit':'LỢI NHUẬN'})

# TRỰC QUAN HÓA DỮ LIỆU WEB APP
app = Dash(__name__)

# app.title = "Finance Data Analysis"
# DỮ LIỆU FIREBASE


app.layout = html.Div(

    children=[
        html.Div(
            children=[
                html.H1(
                    children=["XÂY DỰNG DANH MỤC SẢN PHẨM TÌM NĂNG"],
                    className="header-title",
                    ),
                    ],
            
                ),
            html.Div(
        children=[
                html.H2(
                    children=["20113031-Nguyễn Hồng Phong"]
                    )],
                    className="header-title-2",
            ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H4(children=["DOANH SỐ SALE"]),
                        html.H5(children=tongDoanhSo)# dữa liệu đưa vào
                    ],
                    className="sub-menu",
                ),
                html.Div(
                    children=[
                        html.H4(children=["LỢI NHUẬN"]),
                        html.H5(children=tongLoiNhuan)# dữa liệu đưa vào
                    ],
                    className="sub-menu",
                ),
                html.Div(
                    children=[
                        html.H4(children=["TOP DOANH SỐ"]),
                        html.H5(children=doanhSoCaoNhat)# dữa liệu đưa vào
                    ],
                    className="sub-menu",
                ),
                html.Div(
                    children=[
                        html.H4(children=["TOP LỢI NHUẬN"]),
                        html.H5(children=loiNhuanCaoNhat)# dữa liệu đưa vào
                    ],
                    className="sub-menu",
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                    id='soluong-graph',
                    figure=figDoanhSoTheoNam),# dữa liệu đưa vào
                    className="mycard",
                ),
                html.Div(
                    children=dcc.Graph(
                    id='doanhso-graph',
                    figure=figTiLeDongGopDanhSoTheoTungDoanhMuc),# dữa liệu đưa vào
                    className="mycard",
                ),
                html.Div(
                    children=dcc.Graph(
                    id='soluongdonhang-graph',
                    figure=figLoiNhanTheoNam),# dữa liệu đưa vào
                    className="mycard",
                ),
                html.Div(
                    children=dcc.Graph(
                    id='sunburst-profit',
                    figure=figTiLeDongGopLoiNhanTheoTungDoanhMuc),# dữa liệu đưa vào
                    className="mycard",
                )
            ],
            style={'display': 'flex', 'flex-direction': 'row', 'flex-wrap': 'wrap'},
            className="mywrapper"
        )
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True, port=8090)