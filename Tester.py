from Src.Numeric_tester import reject_nh_t_statistic
from Src.Proportion_tester import reject_nh_z_statistic

from flask import Flask , request, render_template, flash, redirect,g,url_for
import pandas as pd
import os
global data_columns ,groups_tobe_tested, data,groups_col, to_be_observed, type_

def Test(type_,data, groups_col , control_group, test_group, to_be_observed,alpha=0.05 ):
    if type_ == "numeric":
        activity = to_be_observed
        test_result = reject_nh_t_statistic(data, groups_col , control_group, test_group, activity,alpha=0.05 )
    elif type_ == "proportion":
        conversion = to_be_observed
        test_result = reject_nh_z_statistic(data, groups_col , control_group, test_group, conversion,alpha=0.05 )
    return test_result

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'data'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}


def allowed_files(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('tester_app.html',data_columns =[],groups_tobe_tested =[] )

@app.route("/upload", methods = ["POST"])
def upload():
    global data
    if 'csv_file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['csv_file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if not allowed_files(file.filename):
        flash('Invalid file type. Allowed file types are: csv')
        return redirect(request.url)
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    df = pd.read_csv(file_path)
    data = df
    #f"DataFrame received with {len(df)} rows and {len(df.columns)} columns."
    return render_template(
                'tester_app.html',
                data_columns=df.columns,
                test_type=['numeric', 'proportion'],
                groups_tobe_tested=[]
            )


@app.route('/select_test_veri', methods = ["POST"])
def get_var_and_test():
    global groups_col ,to_be_observed,type_,data
    if request.method == "POST":
        groups_col = request.form["groups_col"]
        to_be_observed = request.form["to_be_observed"]
        type_ = request.form["type"]
        return render_template(
                'tester_app.html',
                data_columns= data.columns,
                test_type=['numeric', 'proportion'],
                groups_tobe_tested=data[groups_col].unique()
            )

@app.route('/select_groups_and_test', methods = ["POST"])
def get_groups_and_test():
    if request.method == "POST":
        global data, type_, groups_col,to_be_observed
        test_group = request.form["Treatment_group"] 
        control_group = request.form["Control_group"]
        result = Test(type_,data, groups_col , control_group, test_group, to_be_observed,alpha=0.05 )
        return render_template(
                'tester_app.html',
                data_columns= data.columns,
                test_type=['numeric', 'proportion'],
                groups_tobe_tested=data[groups_col].unique(),
                test_result = result,
                show = True
            )
if __name__ == '__main__':
    app.run(debug=True)