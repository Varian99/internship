import json

def extract_app_info_from_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    app_info_list = []
    for app in data['app']:
        sublist = []
        app_id = app['id']
        sublist.append(app['id'])
        sublist.append(f"{app['in']['nameListener']}_{app_id}")
        for name in app['treat'].values():
            sublist.append(f"{name}_{app_id}")
        sublist.append(f"{app['out']['nameSender']}_{app_id}")
        app_info_list.append(sublist)
    return app_info_list

def main():
    app_info_list = extract_app_info_from_json("data.json")
    print("Informations extraites :")
    print(app_info_list)
if __name__ == "__main__":
    main()