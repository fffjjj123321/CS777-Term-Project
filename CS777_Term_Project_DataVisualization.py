import os
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.components import Table
from pyecharts.charts import WordCloud
from pyecharts.charts import Pie
from pyecharts.charts import Funnel
from pyecharts.options import ComponentTitleOpts
from pyecharts.globals import SymbolType
import json


def getResultJsonFile(dir):
    for file in os.listdir(dir):
        if (file.endswith('.json')):
            return dir + file
    return ''


# 1.Calculate the daily cumulative number of confirmed cases and deaths in the United States
def drawChart_1(index):
    rootDir = './result' + str(index) + '.json/'
    root = getResultJsonFile(rootDir)

    date = []
    cases = []
    deaths = []
    with open(root, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            js = json.loads(line)
            date.append(str(js['date']))
            cases.append(int(js['cases']))
            deaths.append(int(js['deaths']))

    d = (
        Bar()
            .add_xaxis(date)
            .add_yaxis("Cumulative number of confirmed cases", cases, stack="stack1")
            .add_yaxis("Cumulative number of confirmed deaths", deaths, stack="stack1")
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="Daily cumulative"))
            .render("/Users/tang/Desktop/CS777/CS777_Term_Project/Data Visulization Result/result1.html")
    )


# 2.Calculate the daily number of new confirmed cases and deaths in the United States compared with yesterday
def drawChart_2(index):
    rootDir = './result' + str(index) + '.json/'
    root = getResultJsonFile(rootDir)
    date = []
    cases = []
    deaths = []
    with open(root, 'r') as f:
        while True:
            line = f.readline()
            if not line:  
                break
            js = json.loads(line)
            date.append(str(js['date']))
            cases.append(int(js['caseIncrease']))
            deaths.append(int(js['deathIncrease']))

    (
        Line(init_opts=opts.InitOpts(width="1600px", height="800px"))
            .add_xaxis(xaxis_data=date)
            .add_yaxis(
            series_name="New confirmed cases",
            y_axis=cases,
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="Maximum")

                ]
            ),
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="average", name="Average")]
            ),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="The daily number of new confirmed cases and deaths in the United States", subtitle=""),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
            .render("/Users/tang/Desktop/CS777/CS777_Term_Project/Data Visulization Result/result2.html")
    )


# 3.Statistics as of April 18, 2022, The cumulative number of confirmed cases and deaths in US states
def drawChart_3(index):
    rootDir = './result' + str(index) + '.json/'
    root = getResultJsonFile(rootDir)
    allState = []
    with open(root, 'r') as f:
        while True:
            line = f.readline()
            if not line: 
                break
            js = json.loads(line)
            row = []
            row.append(str(js['state']))
            row.append(int(js['totalCases']))
            row.append(int(js['totalDeaths']))
            row.append(float(js['deathRate']))
            allState.append(row)

    table = Table()

    headers = ["State name", "Total cases", "Total deaths", "Death rate"]
    rows = allState
    table.add(headers, rows)
    table.set_global_opts(
        title_opts=ComponentTitleOpts(title="List of confirmed cases and deaths by state in the United States", subtitle="")
    )
    table.render("/Users/tang/Desktop/CS777/CS777_Term_Project/Data Visulization Result/result3.html")


# 4. Find the 10 states with the most confirmed cases in the U.S.
def drawChart_4(index):
    rootDir = './result' + str(index) + '.json/'
    root = getResultJsonFile(rootDir)
    data = []
    with open(root, 'r') as f:
        while True:
            line = f.readline()
            if not line: 
                break
            js = json.loads(line)
            row = (str(js['state']), int(js['totalCases']))
            data.append(row)

    c = (
        WordCloud()
            .add("", data, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
            .set_global_opts(title_opts=opts.TitleOpts(title="The 10 states with the most confirmed cases in the U.S."))
            .render("/Users/tang/Desktop/CS777/CS777_Term_Project/Data Visulization Result/result4.html")
    )



# 5. Find the 10 states with the fewest deaths in the U.S.
def drawChart_5(index):
    rootDir = './result' + str(index) + '.json/'
    root = getResultJsonFile(rootDir)
    data = []
    with open(root, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            js = json.loads(line)
            data.insert(0, [str(js['state']), int(js['totalDeaths'])])

    c = (
        Funnel()
            .add(
            "State",
            data,
            sort_="descending",
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="Last 10 of deaths"))
            .render("/Users/tang/Desktop/CS777/CS777_Term_Project/Data Visulization Result/result5.html")
    )


# 6. Statistics as of April 18, 2022, The fatality rate of the United States
def drawChart_6(index):
    rootDir = './result' + str(index) + '.json/'
    root = getResultJsonFile(rootDir)
    values = []
    with open(root, 'r') as f:
        while True:
            line = f.readline()
            if not line:  
                break
            js = json.loads(line)
            if str(js['state']) == "USA":
                values.append(
                    ["Death(%)", round(float(js['deathRate']) * 100, 2)])
                values.append(
                    ["No-Death(%)", 100 - round(float(js['deathRate']) * 100, 2)])
    c = (
        Pie()
            .add("", values)
            .set_colors(["blcak", "orange"])
            .set_global_opts(title_opts=opts.TitleOpts(title="The fatality rate of the United States"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .render("/Users/tang/Desktop/CS777/CS777_Term_Project/Data Visulization Result/result6.html")
    )


index = 1
while index < 7:
    funcStr = "drawChart_" + str(index)
    eval(funcStr)(index)
    index += 1