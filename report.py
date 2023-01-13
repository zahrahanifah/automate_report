import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
from plugins.send_to_slack import send_to_slack
from plugins.transform.read_transform import run_transform
from plotly.subplots import make_subplots
from datetime import datetime
from datetime import date

def run():
    file_bytes = "C:/Users/zahra.hanifah/Downloads/Zahra/000 Learning/DE Bootcamp/automate_report/output/report_ticket.png"

    # analyze and create graph
    data = run_transform('C:/Users/zahra.hanifah/Downloads/Zahra/000 Learning/DE Bootcamp/automate_report/data')

    summarize_open_ticket = data[data['status']=='Open'].groupby(['ticket_status'])['ticket_status'].count().to_frame(name = 'count').reset_index()
    summarize_status = data.groupby(['status'])['status'].count().to_frame(name = 'count').reset_index()

    #count ticket
    total_ticket = len(data)
    open_ticket = len(data[data["status"]=="Open"])
    resolved_ticket = len(data[data["ticket_status"]=="Resolved"])
    queue_ticket = len(data[data["ticket_status"]=="On-Queue"])
    onprogress_ticket = len(data[data["ticket_status"]=="On-Progress"])

    #colors doughnut chart
    colors = ['#ff9999','#66b3ff','#FFDB89','#ffcc99']

    #create function for dougnut chart
    def get_doughnut_chart(labels, size):    
        pie = go.Pie(labels=labels, values=size, hole=.5, marker=dict(colors=colors))
        pie.marker.line.width = 10
        pie.marker.line.color = 'white'
        pie.textposition = 'outside'
        pie.textinfo = 'label+percent'
        pie.showlegend = False

        return pie

    #create chart
    trace_status = get_doughnut_chart(summarize_status['status'], summarize_status['count'])
    trace_open_ticket = get_doughnut_chart(summarize_open_ticket['ticket_status'], summarize_open_ticket['count'])

    #  make subplot for two chart 
    fig = make_subplots(
        rows=1, 
        cols=2 ,
        specs=[[{"type": "pie"}, {"type": "pie"}]])

    traces = dict()
    traces["overall_status"] = trace_status
    traces["open_ticket"] = trace_open_ticket

    fig.append_trace(traces["overall_status"],1,1)
    fig.append_trace(traces["open_ticket"],1,2)   

    # create chart title
    today = date.today().strftime("%B %d, %Y")
    large_title_format = "<span style='font-size:30px; font-family:Times New Roman'>IT Ticket Support Report</span>"
    small_title_format = f"<span style='font-size:16px; font-family:Times New Roman'>{today}</b></span>"

    layout = dict(
        title = large_title_format + "<br>" + small_title_format,
        font = dict(color = 'black'),
        showlegend = False,
        margin = dict(t=150,pad=6),
        plot_bgcolor='#fff',
        bargap = 0.20,)

    fig['layout'].update(layout)

    #add annotation 1
    large_ann1 = f"<span style='font-size:40px; font-family:Times New Roman'>{str(total_ticket)}</span>"
    small_ann1 = "<span style='font-size:17px; font-family:Times New Roman'>Total Ticket</b></span>"

    fig.add_annotation(x=0.17
    , y=0.5
    , text= large_ann1 + "<br><br>" + small_ann1
    , showarrow=False
    , ax=-20
    , ay=-30
    , align="center"
    ,)

    #add annotation 2
    large_ann1 = f"<span style='font-size:40px; font-family:Times New Roman'>{str(open_ticket)}</span>"
    small_ann1 = "<span style='font-size:17px; font-family:Times New Roman'>Open Ticket</b></span>"

    fig.add_annotation(x=0.83
    , y=0.5
    , text= large_ann1 + "<br><br>" + small_ann1
    , showarrow=False
    , ax=-20
    , ay=-30
    , align="center"
    ,)


    fig.show()

    # Save graph ke image png
    pio.write_image(fig, file_bytes, width=1000, height=500)

    # send graph to slack channel
    class status_message:
        desc = "ticket"
        
        def __init__(self,total_ticket,open_ticket):
            self.total_ticket = total_ticket
            self.open_ticket = open_ticket
        
        @staticmethod
        def full_closed():
             return("All ticket are closed")
        
        def partially_closed(self):
             return(f"We still have {self.open_ticket} open ticket!!")

    it_support = status_message(total_ticket,open_ticket)

    if open_ticket == 0:
        message = it_support.full_closed()
    else:
        message = it_support.partially_closed()

    channel = "#automate_report"

    send_to_slack.execute(message, channel, file_bytes)

if __name__ == '__main__':
    run()