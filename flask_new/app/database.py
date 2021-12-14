"""Defines all the functions related to the database"""
from yaml import serialize
from app import db
from app.utils import *
import os
import datetime  


'''
name of functions:
<sql operation name>_<which table>
'''


def insert_new_RateVideo(text: str) ->  int:

    conn = db.connect()
    query = 'Insert Into RateVideo (VideoId,UserId,Rate,TIMESTAMP_R) VALUES ("{}", "{}", "{}", "{}");'.format(
        *text.split(',')) 
    conn.execute(query) # Will trigger
    query_results = conn.execute("Select LAST_INSERT_ID();")  # which one?
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id

def delete_new_RateVideo(user_id: int, movie_id: int) ->  int:
    
    conn = db.connect()
    query = 'Delete From RateVideo where UserId={} and VideoId={};'.format(user_id, movie_id)
    conn.execute(query)
    conn.close()

def Update_new_RateVideo(user_id: int, movie_id: int, rate: float) ->  int:
    
    conn = db.connect()
    query = 'Update RateVideo set Rate = {} where VideoId = {} and UserId={};'.format(rate, movie_id, user_id)
    conn.execute(query)
    conn.close()

def update_movie_score(user_id:int, movie_id: int, rate: float) ->  int:
    timenow = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    conn = db.connect()
    movie_id = int(movie_id)
    user_id = int(user_id)
    # Whether we have this movie
    query = 'select VideoId from RateVideo where VideoId={}'.format(movie_id)
    item = conn.execute(query)
    item = [x for x in item]
    print(item)
    if item != []:
        query = 'select VideoId from RateVideo where VideoId={} and UserId={}'.format(movie_id, user_id)
        item = conn.execute(query)
        item = [x for x in item]
        if item != []:
            query = 'Update RateVideo SET `Rate`={}, `TIMESTAMP_R`="{}" where `UserId`={} and `VideoId`={};'.format(rate,timenow, user_id,movie_id)
            conn.execute(query)
        else: 
            query = 'Insert Into RateVideo (`VideoId`,`UserId`,`Rate`,`TIMESTAMP_R`) VALUES ({},{},{},"{}");'.format(movie_id, user_id, rate, timenow) 
            conn.execute(query) # Will trigger
    conn.close()
    return movie_id




'''
homepage, the category table modification backend
'''

def fetch_category() -> dict:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """
    conn = db.connect()
    query_results = conn.execute("Select * from Category;").fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "CategoryId": result[0],
            "CategoryType": result[1],
            "CategoryName": result[2],
            "CategoryDescription": result[3],
        }
        todo_list.append(item)

    return todo_list


def update_category_description(task_id: int, text: str) -> None:
    """ Updates task description based on given 'task_id'

    Args:
        task_id (int): Targeted task_id
        text (str): Updated description

    Returns:
        None
    """
    #print(task_id)
    conn = db.connect()
    query = 'Update Category set CategoryDescription = "{}" where CategoryId = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()

def insert_new_category(text: str) ->  int:
    """Insert new task to todo table.

    Args:
        text (str): Task description

    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    # query = 'Insert Into tasks (task, status) VALUES ("{}", "{}");'.format(
    #     text)
    query = 'Insert Into Category (CategoryId,CategoryType,CategoryName,CategoryDescription) VALUES ("{}", "{}", "{}", "{}");'.format(
        *text.split(','))
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id


def remove_category_by_id(task_id: int) -> None:
    """ remove entries based on task ID """
    conn = db.connect()
    query = 'Delete From Category where CategoryId={};'.format(task_id)
    conn.execute(query)
    conn.close()

def search_category(condition):
    conn = db.connect()
    condition = condition.replace("%", "%%")
    query_results = conn.execute("Select * from Category where {};".format(condition))
    conn.close()
    item_list = []
    for result in query_results:
        item = {
            "CategoryId": result[0],
            "CategoryType": result[1],
            "CategoryName": result[2],
            "CategoryDescription": result[3]
        }
        item_list.append(item)
    return item_list

'''
login page backend
'''
def validate_user_login(data):
    user = data["user"]
    password = data["password"]
    match_users_sql = "Select UserId, UserName From User Where {}={} AND Password={};"
    conn = db.connect()
    query = ''
    if user.isdigit():
        query = match_users_sql.format("UserId", user, '''"'''+password+'''"''')
    elif '@' in user:
        query = match_users_sql.format("Email", '''"'''+user+'''"''', '''"'''+password+'''"''')
    else:
        query = match_users_sql.format("UserName", '''"'''+user+'''"''', '''"'''+password+'''"''')
    print(query)
    result = conn.execute(query)
    cnt = 0
    res = {"status": "failure", "UserName":"", "UserId": ""}
    for row in result:
        if cnt == 1:
            break
        cnt += 1
        res["status"] = "success"
        res["UserId"] = row[0]
        res["UserName"] = row[1]
    conn.close()
    return res


'''
category page backend
'''
def fetch_video_rate(name: str,limit: int) -> dict:
    #print(name, limit)
    name = name.replace("%", "%%")
    conn = db.connect()
    query = 'SELECT v.VideoId, v.VideoName, v.OriginalName, v.VideoDescription, v.StartYear, v.EndYear, v.RuntimeMinutes, c.CategoryName, r.RateAvg \
        FROM (SELECT * \
        FROM Video  \
        WHERE VideoName LIKE "{}") v  \
        NATURAL JOIN Category c LEFT JOIN \
        (SELECT VideoId, AVG(Rate) As RateAvg \
        FROM RateVideo \
        Group BY VideoId \
        ORDER BY RateAvg DESC, VideoId) r ON v.VideoId = r.VideoId \
        ORDER BY ISNULL(r.RateAvg), r.RateAvg DESC, v.VideoId \
        LIMIT {};'.format(name, limit)
    # query = 'SELECT v.VideoId, v.VideoName, v.OriginalName, v.VideoDescription, v.StartYear, v.EndYear, v.RuntimeMinutes, c.CategoryName, r.RateAvg \
    #     FROM Video v NATURAL JOIN Category c NATURAL JOIN \
    #     (SELECT VideoId, AVG(Rate) As RateAvg \
    #     FROM RateVideo \
    #     Group BY VideoId \
    #     ORDER BY RateAvg DESC, VideoId \
    #     LIMIT {}) r \
    #     ORDER BY VideoId;'.format(limit)
    #print(query)
    query_results = conn.execute(query).fetchall()
    conn.close()
    #print(query_results)
    #return query_to_table(query_results, "/video/")
    video_rate_list = []
    for result in query_results:
        item = {
            "VideoId": result[0],
            "VideoName": result[1],
            "OriginalName": result[2],
            "VideoDescription": result[3],
            "StartYear": result[4],
            "EndYear": result[5],
            "RuntimeMinutes": result[6],
            "CategoryName": result[7],
            "RateAvg": result[8],
        }
        video_rate_list.append(item)
    return video_rate_list
    '''
    video_rate_string = ''
    for result in query_results:
        video_rate_string += "<tr>"
        for entry in result:
            movie_rate_string += "<td>"
            movie_rate_string += str(entry)
            movie_rate_string += "</td>"
        video_rate_string += "</tr>"
    return video_rate_string
    '''

def fetch_single_video(VideoId: int):
    query1 = 'SELECT * FROM (SELECT * FROM Video WHERE VideoId = {}) v NATURAL JOIN Category;'.format(VideoId)
    query2 = 'SELECT * FROM (SELECT * FROM Participate WHERE VideoId = {}) p NATURAL JOIN People;'.format(VideoId)
    query3 = 'SELECT AvgRate FROM AvgRateVideo where VideoId={};'.format(VideoId)
    conn = db.connect()
    result1 = conn.execute(query1).fetchall()
    result2 = conn.execute(query2).fetchall()
    result3 = conn.execute(query3).fetchall()
    conn.close()
    result1 = result1[0]
    result3 = result3[0]
    item = {
        "VideoId": result1[1],
        "VideoName": result1[2],
        "OriginalName": result1[3],
        "VideoDescription": result1[4],
        "StartYear": result1[5],
        "EndYear": result1[6],
        "RuntimeMinutes": result1[7],
        "CategoryId": result1[0],
        "CategoryName": result1[9],
        "CategoryDescription": result1[10],
        "AvgRate":result3[0]
    }
    #print(item)
    people = []
    for result in result2:
        entry = {
            "PeopleId": result[0],
            "VideoId": result[1],
            "ParticipateDescription": result[2],
            "PeopleName": result[3],
            "BirthYear": result[4],
            "DeathYear": result[5],
            "PeopleDescription": result[6],
        }
        people.append(entry)
    #print(people)
    return item, people

def fetch_single_actor(People: int):
    query1 = 'SELECT * FROM People WHERE PeopleId = {}'.format(People)
    conn = db.connect()
    result1 = conn.execute(query1).fetchall()
    conn.close()
    result1 = result1[0]
    item = {
        "PeopleName": result1[1],
        "BirthYear": result1[2],
        "DeathYear": result1[3]
    }
    return item


def find_best_movies():
    query1 = 'CALL SelectBestMovie();'
    query2 = 'SELECT * FROM BestMovies LIMIT 10;'
    conn = db.connect()
    result1 = conn.execute(query1)
    result2 = conn.execute(query2).fetchall()
    best_movies_list = []
    for movie in result2:
        entry = {
            "VideoId": movie[0],
            "VideoName": movie[1],
            "RateAvg": movie[2]
        }
        best_movies_list.append(entry)
    conn.close()
    print(best_movies_list)
    return best_movies_list

def find_best_actors():
    query1 = 'CALL SelectBestActor();'
    query2 = 'SELECT * FROM BestActors LIMIT 10;'
    conn = db.connect()
    result1 = conn.execute(query1)
    result2 = conn.execute(query2).fetchall()
    best_actor_list = []
    for actor in result2:
        entry = {
            "PeopleId": actor[0],
            "PeopleName": actor[1],
            "RateAvg": actor[2]
        }
        best_actor_list.append(entry)
    conn.close()
    print("TEST")
    print(best_actor_list)
    return best_actor_list


# # Used for testing
# def find_best_actors():
#     query = 'SELECT PeopleId, PeopleName FROM People WHERE PeopleId > 37578 AND PeopleId < 37588;'
#     conn = db.connect()
#     result1 = conn.execute(query).fetchall()
#     best_actor_list = []
#     for actor in result1:
#         entry = {
#             "PeopleId": actor[0],
#             "PeopleName": actor[1],
#             "RateAvg": 10
#         }
#         best_actor_list.append(entry)
#     conn.close()
#     print("TEST")
#     print(best_actor_list)
#     return best_actor_list
