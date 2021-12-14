""" Specifies routing for the application"""
from os import removedirs
from flask import render_template, request, jsonify, redirect, make_response
from app import app
from app import database as db_helper

'''
name of functions:
<web page name>_<operation>
'''

'''
home page
'''
@app.route("/")
def home_page():
    # username = request.cookies.get("username")
    # if username == None:
    #     username=""
    #     return render_template("index.html", username = username)
    # return render_template("index.html", username = username+" :")
    print(request.cookies.get("userid"))
    return render_template("index.html")

@app.route("/homesearch")
def home_search():
    return jsonify({'success': True, 'response': 'finish search'})

'''
category page
'''
@app.route("/category.html")
def category_page():
    """ returns rendered homepage """
    items = db_helper.fetch_category()
    username = request.cookies.get("username")
    if username == None:
        username=""
        return render_template("category.html", items=items, username = username)
    return render_template("category.html", items=items, username = username+": ")

@app.route("/delete/<int:task_id>", methods=['POST'])
def category_delete(task_id):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_category_by_id(task_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/edit/<int:task_id>", methods=['POST'])
def category_update(task_id):
    """ recieved post requests for entry updates """
    data = request.get_json()
    try:
        if "description" in data:
            db_helper.update_category_description(task_id, data["description"])
            result = {'success': True, 'response': 'Task Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/create", methods=['POST'])
def category_create():
    """ recieves post requests to add new task """
    data = request.get_json()
    #print(data)
    db_helper.insert_new_category(data['description'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route("/search/<condition>", methods=['GET'])
def category_search(condition):
    # condition = request.get_json()
    items = []
    try:
        items = db_helper.search_category(condition)
        # return render_template("index.html", items=items)
        result = {'success': True, 'response': 'Done'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}
    return render_template("index.html", items=items)

'''
login page
'''
@app.route("/login.html")
def login_page():
    username = request.cookies.get("username")
    if username == None:
        username=""
        return render_template("login.html", username = username)
    return render_template("login.html", username = username+": ")

@app.route("/loginvalidation", methods=['POST'])
def login_validate():
    data = request.get_json()
    # print(data)
    try:
        ret = db_helper.validate_user_login(data)
        if ret["status"] == "success":
            result = {'success': True, 'response': 'login successful', 'UserName':ret["UserName"], "UserId": ret["UserId"]}
        else:
            result = {'success': False, 'response': 'cannot login', 'UserName':"None", "UserId": "None"}
    except:
        # print("execution error")
        result = {'success': False, 'response': 'cannot login', 'UserName':"None", "UserId": "None"}
    return jsonify(result)

@app.route("/logout")
def logout():
    print("TESTLOG")
    new_url = "/"
    resp = redirect(new_url)
    resp.delete_cookie("username")
    resp.delete_cookie("userid")
    return resp

@app.route("/bestmovies")
def bestmovies():
    items = db_helper.find_best_movies()
    username = request.cookies.get("username")
    if username == None:
        return render_template("bestvideo.html", items=items, username="")
    return render_template("bestvideo.html", items=items, username=username+": ")

@app.route("/bestactors")
def bestactors():
    items = db_helper.find_best_actors()
    username = request.cookies.get("username")
    if username == None:
        return render_template("bestactor.html", items=items, username="")
    return render_template("bestactor.html", items=items, username=username+": ")

'''
video page
'''
@app.route("/video.html")
def video_page():
    """ returns rendered video.html """
    #items = db_helper.fetch_video_rate(100)
    #return render_template("video.html", items=items)
    username = request.cookies.get("username")
    if username == None:
        username=""
        return render_template("video.html", username = username)
    return render_template("video.html", username = username+": ")

@app.route("/video/search/<name>/<int:limit>.html", methods=['GET'])
def video_search(name, limit):
    #print(name, limit)
    items = []
    try:
        items = db_helper.fetch_video_rate(name, limit)
        #result = {'success': True, 'response': 'Removed task'}
    except:
        items = []
        #result = {'success': False, 'response': 'Something went wrong'
    username = request.cookies.get("username")
    # print(items)
    # print(username)
    ret = None
    if username == None:
        username = ""
        ret = render_template("video.html", items=items, username = username)
    else:
        ret = render_template("video.html", items=items, username = username+": ")
    return ret

'''
video subpage
'''
@app.route("/video/<int:VideoId>.html")
def single_video_page(VideoId):
    item, people = db_helper.fetch_single_video(VideoId)
    username = request.cookies.get("username")
    if username == None:
        username=""
        return render_template("video_page.html", item=item, people=people, username = username)
    return render_template("video_page.html", item=item, people=people, username = username+": ")

@app.route("/actor/<int:PeopleId>.html")
def single_actor_page(PeopleId):
    item = db_helper.fetch_single_actor(PeopleId)
    username = request.cookies.get("username")
    if username == None:
        username=""
        return render_template("people_page.html", item=item,  username = username)
    return render_template("people_page.html", item=item,username = username+": ")

'''
video index subpage
'''

@app.route("/video/rate/<condition>", methods=['GET'])
def single_movie_score(condition):
    userid= request.cookies.get("userid")
    datanew = condition.split(",")
    MovieId = int(datanew[0])
    Rate = float(datanew[1])
    if Rate>10 or Rate<0:
        return render_template("index.html")
    item = db_helper.update_movie_score(userid,MovieId,Rate)
    print("success")
    # item = db_helper.fetch_single_actor(Rate)
    # username = request.cookies.get("username")
    # if username == None:
    #     username=""
    #     return render_template("video_page.html", item=item,  username = username)
    # return render_template("video_page.html.html", item=item,username = username+": ")
    return render_template("index.html")

@app.route("/video/edit/<condition>", methods=['GET'])
def delete_movie_score(condition):
    userid= request.cookies.get("userid")
    MovieId = int(condition)
    db_helper.delete_new_RateVideo(userid,MovieId)
    print("success")
    # item = db_helper.fetch_single_actor(Rate)
    # username = request.cookies.get("username")
    # if username == None:
    #     username=""
    #     return render_template("video_page.html", item=item,  username = username)
    # return render_template("video_page.html.html", item=item,username = username+": ")
    return render_template("index.html")

