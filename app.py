from fetch_data import FetchBlogData
from flask import Flask, make_response, jsonify, request
from blog_api_logging import BlogApiLog

app = Flask(__name__)
logger = BlogApiLog("fetch_data.py", "blog_api.log")
logger = logger.get_logger()


@app.route('/ping', methods=['GET'])
def ping():
    data = {"success": True}
    return make_response(jsonify(data), 200)


@app.route('/', methods=['GET'])
def home():
    data = {"success": True}
    return make_response(jsonify(data), 200)


@app.route('/posts')
def get_posts():
    SORT_BY_VALUES = ["id", "reads", "likes", "popularity"]
    # checking if a key other than tags, sortBy and direction was used
    logger.info(request.args)
    for key in request.args:
        if key != "tags" and key!="sortBy" and key!="direction":
            data = {"error": "Unknown parameter : '{}'. Please use tags or sortBy or direction only".format(key)}
            logger.info("user provided => {}. Response => {}".format(request.args,data))
            return make_response(jsonify(data), 400)

    tags = request.args.get('tags')
    sort_by = request.args.get('sortBy')
    direction = request.args.get('direction')


    if tags:
        tag_list = tags.lower().split(",")
    else:
        # tags are not mentioned by user return error
        data = {"error": "Tags parameter is required"}
        logger.info("user provided => {}. Response => {}".format(request.args, data))
        return make_response(jsonify(data), 400)

    # checking if sortBy values are valid
    if not sort_by:
        sort_by = "id"
    elif sort_by.lower() not in SORT_BY_VALUES:
        data = {"error": "SortBy parameter is invalid"}
        logger.info("user provided => {}. Response => {}".format(request.args, data))
        return make_response(jsonify(data), 400)

    descending = False

    if not direction or direction.lower() == "asc":
        descending = False
    elif direction != "desc" and direction != "asc":
        data = {"error": "direction parameter is invalid"}
        logger.info("user provided => {}. Response => {}".format(request.args, data))
        return make_response(jsonify(data), 400)
    elif direction.lower() == "desc":
        descending = True

    fetch_object = FetchBlogData(tag_list, sort_by, descending)
    result = fetch_object.fetch()
    if len(result) == 0:
        data = {"posts": []}
        logger.info("user provided => {}. Response => {}".format(request.args, data))
        return make_response(jsonify(data), 200)
    elif result[0] == "website down":
        data = {"error": "service unavailable"}
        logger.exception("Parent API service Unavailable")
        return make_response(jsonify(data), 503)
    else:
        data = {"posts": result}
        logger.debug("user provided => {}. Response => {}".format(request.args, data))
        return make_response(jsonify(data), 200)


if __name__ == '__main__':
    # this list maintains sortBy values that are acceptable
    app.run()
