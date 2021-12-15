#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Ren Qiang'
# %% 绘图

import os
import time
import pandas as pd
from pyecharts.charts import Line, Grid, Page
import pyecharts.options as opts


def plot_msg():
    df = pd.read_excel('./output/spider_beike.xlsx',
                       sheet_name='beike', index_col=0)  # 读取excel数据文件)
    # 过滤房价为0的无效数据
    df = df[df.totalPrice > 0]
    # # 去除重复行
    df = df.drop_duplicates()
    for district in df.district.unique():
        df2 = df[df.district == district]
        page = Page()  # layout=Page.DraggablePageLayout
        # grid = Grid()
        for address in df2.address.unique():
            df_address = df2[df2.address == address].filter(
                items=['time', 'housedel_id', 'totalPrice']).sort_values(by='time', ascending=True)
            x = [str(x)[0:10] for x in df_address.time.unique()]
            legend = df_address.housedel_id.unique().tolist()
            max_df_address = df_address.totalPrice.max()
            min_df_address = df_address.totalPrice.min()
            delta = max_df_address-min_df_address
            line = (
                Line()
                .add_xaxis(xaxis_data=x)
                .set_global_opts(title_opts=opts.TitleOpts(title="小区：\n{}".format(address)),
                                yaxis_opts=opts.AxisOpts(min_=(min_df_address//10-1)*10,
                                                        max_=(max_df_address//10+1)*10))
            )
            for legend_i in legend:
                line_ = (
                    Line()
                    .add_xaxis(xaxis_data=x)
                    .add_yaxis(series_name=str(legend_i), is_smooth=True, is_hover_animation=True,
                            y_axis=df_address[df_address.housedel_id == legend_i].totalPrice.tolist())
                )

                line.overlap(line_)  # 堆叠
            page.add(line)
        page.render('./output/totalPrice-address-{0}.html'.format(district))
    return


if __name__ == '__main__':
    
    plot_msg()

# %%
