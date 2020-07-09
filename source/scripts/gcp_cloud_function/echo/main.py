def echo(request):
    import flask

    data = {"success": False}
    params = request.get_json()

    if "msg" in params:
        data["response"] = str(params['msg'])
        data["success"] = True
    
    return flask.jsonify(data)