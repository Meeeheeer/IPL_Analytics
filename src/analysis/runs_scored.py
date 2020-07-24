import pymongo
import pandas as pd
import matplotlib.pyplot as plt

def main():
    myClient = pymongo.MongoClient("mongodb://localhost:27017")
    myDb= myClient['IPL']
    RunsScored = myDb['runs_scored']


    start=int(input('enter the starting over(min 1, max 20) :'))
    stop=int(input('enter the ending over (should be greater than the starting over max 20) :'))
    season=int(input('enter the season between [2008---2019] :'))
    innings=int(input('enter innings [1,2] :' ))

    avg_overs={'_id':'$team'}
    
    query=[
        {'$match':{
                'season':season,
                '$and':[{'over':{'$gte':start}},{'over':{'$lte':stop}}],
                'innings':innings
                }
        },
        {'$group':{
                '_id': {'team':"$batting_team",'over':"$over"},
                'averageRunsOver': {
                    '$avg': "$runs"
                                }
                }
        },
        {'$sort':{
            "_id.over": 1
                }

        }
        ]

    runs_by_team=list(RunsScored.aggregate(query))
    overs=[i for i in range(start,stop+1)]
    df_dict={'overs':overs}

    
    for team in runs_by_team:
        try:
            df_dict[team['_id']['team']].append(team['averageRunsOver'])
        except:
            df_dict[team['_id']['team']]=[team['averageRunsOver'],]
            

    
    
    df=pd.DataFrame.from_dict(df_dict)
    print(df)


    teams=list(df.columns)
    teams.remove('overs')

    if innings==1:
        inng='1st'
    else:
        inng='2nd'

    ax=df.plot.line(x='overs',y=teams,\
        title='Average runs scored by teams batting {} the between overs {} and {} in season {} '.format(start,stop,season,inng))
    ax.set_ylabel("average_runs")
    plt.show()
    
    
    
    

if __name__ =='__main__':
    main()