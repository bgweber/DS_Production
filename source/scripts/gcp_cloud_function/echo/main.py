def echo(request):
    from flask import jsonify

    data = {"success": False}
    params = request.get_json()

    if "msg" in params:
        data["response"] = str(params['msg'])
        data["success"] = True
    
    return jsonify(data)