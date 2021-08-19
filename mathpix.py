import requests
import json


def precise_detection(image_path):
    r = requests.post("https://api.mathpix.com/v3/latex",
                      files={"file": open(image_path, "rb")},
                      data={"options_json": json.dumps({
                          "formats": ["latex_simplified", "asciimath"]
                      })},
                      headers={
                          "app_id": "jiehong0914_gmail_com_5c184a_c43c25",
                          "app_key": "caed2c40152d7d6d3d9c293757ae0d904cab819453f0840e27e3700efe6c5292"
                      }
                      )
    resp = (r.json())
    # print(json.dumps(r.json(), indent=4, sort_keys=True))
    return resp["latex_simplified"]


# resp = {'request_id': 'af58ac2c7cc84687cc406525fea3603f', 'detection_map': {'contains_chart': 0, 'contains_diagram': 0, 'contains_graph': 0, 'contains_table': 0, 'is_blank': 0, 'is_inverted': 0, 'is_not_math': 0, 'is_printed': 0.0025909794494509697}, 'detection_list': [],
#         'auto_rotate_confidence': 0.01977018111795914, 'auto_rotate_degrees': 0, 'position': {'top_left_x': 474, 'top_left_y': 372, 'width': 606, 'height': 156}, 'latex_confidence': 0.9765625, 'latex_confidence_rate': 0.9966517857142857, 'latex_simplified': '1 + 2 / 5 \\times 3', 'asciimath': '1+2/5times3'}

# print(resp["latex_simplified"])
