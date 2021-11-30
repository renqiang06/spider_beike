#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Ren Qiang'
# %% 绘图
import pandas as pd
import os
import time
from pyecharts.charts import Line, Grid, Page
import pyecharts.options as opts


def plot_msg():
    df = pd.read_excel('./output/spider_beike.xlsx',
                       sheet_name='beike', index_col=0)  # 读取excel数据文件)

    # 过滤房价为0的无效数据
    df = df[df.totalPrice > 0]
    # # 去除重复行
    df = df.drop_duplicates()
    # page = Page()
    # grid = Grid()
    for address in df.address.unique():
        _i = 1
        df_address = df[df.address == address].filter(
            items=['time', 'housedel_id', 'totalPrice']).sort_values(by='time', ascending=True)
        x = [str(x)[0:10] for x in df_address.time.unique()]
        legend = df_address.housedel_id.unique().tolist()

        line = (
            Line()
            .add_xaxis(xaxis_data=x)
            .set_global_opts(title_opts=opts.TitleOpts(title="走势"))
        )
        for legend_i in legend:
            line_ = (
                Line()
                .add_xaxis(xaxis_data=x)
                .add_yaxis(series_name=str(legend_i),
                           y_axis=df_address[df_address.housedel_id == legend_i].totalPrice.tolist(), is_symbol_show=False,
                           is_connect_nones=True, linestyle_opts=opts.LineStyleOpts(width=2), label_opts=opts.LabelOpts(is_show=False),)
            )

            line.overlap(line_)  # 堆叠
        line.render('{}.html'.format(address))
    #     page.add(line)
    # page.render('test.html')
    return


if __name__ == '__main__':
    plot_msg()

# %%
