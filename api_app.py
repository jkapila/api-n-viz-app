from flask import Flask
from flask import jsonify
from flask_restful import Api, Resource, reqparse
from flask_restful import fields, marshal_with
import json

import numpy as np
import pandas as pd
import os


### doing processing
df = pd.DataFrame({"style_J":[.3,.2,0.2,0.3],
                  "style_K":[.2,.2,0.1,0.3],
                  "style_L":[.5,0,0.5,0.05],
                  "style_M":[0,.6,0.2,0.35]},index = ["A","B","C","D"])

df.to_csv(os.path.join(os.getcwd(),'data','distribution_file.csv'))
df_samp = pd.read_csv(os.path.join(os.getcwd(),'data','Inventory.csv'))
df_samp['Forecasted Claims(TE)'] = np.round(df_samp['Forecasted Claims(TE)'],2)

def append_multiple_lines(file_name, lines_to_append):
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        appendEOL = False
        # Move read cursor to the start of file.
        file_object.seek(0)
        # Check if file is not empty
        data = file_object.read(100)
        if len(data) > 0:
            appendEOL = True
        # Iterate over each string in the list
        for line in lines_to_append:
            # If file is not empty then append '\n' before first line for
            # other lines always append '\n' before appending line
            if appendEOL == True:
                file_object.write("\n")
            else:
                appendEOL = True
            # Append element at the end of file
            file_object.write(line)


            
# main flask app
app = Flask(__name__)
api = Api(app)

@app.route('/distr')
def get_distribution():
    return df.to_json(orient="index")

@app.route('/evaluate/<string:inp>')
def evaluate(inp):
    file_path = os.path.join(os.getcwd(),'data','input.txt')
    append_multiple_lines(file_path,[inp])
    df_samp['Simulated Claims(TE)'] = np.round(df_samp['Forecasted Claims(TE)']* np.random.random(),2)
    return df_samp.to_json(orient="columns")
    
          
          
# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('distr', help='Distribution of Style in Group')
parser.add_argument('fcode', type=str, help='Describe Group')
resource_fields = {'fcode': fields.String, 'distr': fields.List(fields.Float)}
         
class Item(Resource):
    @marshal_with(resource_fields, envelope='resource')
    def get(self, **kwargs):
        args = parser.parse_args()
        distr = args['distr']  # List [0.25,0.25,0.25,0.25]
        distr =[float(x) for x in distr.split(',')]
        fcode = args['fcode'] # Boolean True
        print(f"Group: {fcode} Current Distr: {df.loc[fcode,:]} Update Distr: { distr}")
        if sum(distr) != 1.:
            raise ValueError("Sum should be equal to 1")
        
        
        for c,v in zip(['J','K','L','M'],distr):
            df.loc[fcode,f'style_{c}'] = v
        return df.to_json(orient="columns")
    
    def put(self):
        return jsonify(df.to_json(orient="index"))

api.add_resource(Item, '/update')
         


# steps:
# http://10.0.0.2:105/distr
# http://10.0.0.2:105/update?fcode=A&distr=0.1,0.1,0.1,0.7
# http://10.0.0.2:105/distr        

if __name__ == '__main__':
    print('Current Distribution of style per group')
    print(df.to_json(orient="index"))
    app.run(host='0.0.0.0', port=8000)
