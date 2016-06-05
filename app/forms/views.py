from flask import render_template, redirect, request, Blueprint, url_for
import config
from utils.helpers import semiflatten
from models import FormData, FormLink, Thread, InboundData
from forms import CreatFormLink
from flask_login import login_required, current_user
import sendgrid
import re

sg = sendgrid.SendGridClient(config.SG_USER, config.SG_PASSWORD)

forms = Blueprint('forms', __name__)


@forms.route('/')
def index():
    return render_template('index.html')


@forms.route('/data')
@login_required
def dashboard():
    formlinks = None
    if current_user.is_authenticated:
        formlinks = FormLink.objects(creator=current_user.to_dbref())

    return render_template('forms/dashboard.html', formlinks=formlinks)


@forms.route('/form/<int:fid>', methods=['GET', 'POST'])
def form(fid):
    if FormLink.objects(fid=fid):
        if request.method == 'POST':
            form_data = FormData()
            formlink = FormLink.objects(fid=fid).first().to_dbref()
            form_data.thread = Thread(formlink=formlink).save()
            form_data.load = semiflatten(request.form)
            form_data.headers = dict(request.headers.items())
            form_data.ip = request.remote_addr
            form_data.save()
            return redirect(url_for('forms.data', fid=fid))

        return render_template('forms/test_form.html',
                               fid=url_for('forms.form', fid=fid))
    else:
        return 'no form found'


@forms.route('/inbound/', methods=['POST', 'GET'])
def inbound():
    if request.method == 'POST':
        InboundData(raw=request.form).save()
        text = None
        subject = request.form['subject'].decode('utf-8')
        print subject
        reg = re.compile(ur"[\[]DFNR:(\d+)[-](\d+)[\]]".decode('utf-8'))
        fid = int(re.search(reg, subject).group(1))
        tid = int(re.search(reg, subject).group(2))
        if request.form['text']:
            text = request.form['text'].split('\n')[0]

        form_data = FormData()
        form_data.thread = Thread.objects(tid=tid).first().to_dbref()
        form_data.load = {'message': text}
        form_data.save()
    return ''


@forms.route('/data/<int:fid>')
def data(fid):
    formlinks = FormLink.objects(creator=current_user.to_dbref())
    formlink = FormLink.objects(fid=fid).first()
    # print 'formlink:', formlink
    threads = Thread.objects(formlink=formlink)
    return render_template('forms/dashboard.html', fid=fid,
                           threads=threads, formlinks=formlinks)


@forms.route('/data/<int:fid>/thread/<int:tid>')
def data_view(fid, tid):
    formlinks = FormLink.objects(creator=current_user.to_dbref())
    formlink = FormLink.objects(fid=fid).first()
    # print 'formlink:', formlink
    threads = Thread.objects(formlink=formlink)
    thread = Thread.objects(tid=tid).first()
    datas = FormData.objects(thread=thread).order_by('id')
    main = FormData.objects(thread=thread).order_by('id').first()
    # for x in mains:
    #     print 'hhhhhh', x.load
    # main =  None
    return render_template('forms/dashboard.html', fid=fid, datas=datas,
                           threads=threads, formlinks=formlinks, tid=tid, main=main)


@forms.route('/form/create/', methods=['POST'])
def create_form():
    form = CreatFormLink()
    if request.method == 'POST' and form.validate():
        formlink = FormLink(name=form.name.data,
                            creator=current_user.to_dbref())
        formlink.save()
        return redirect('/data')
    return redirect('/data')


@forms.route('/data/<int:fid>/thread/<int:tid>/email', methods=['POST'])
def send_email(fid, tid):
    body = request.form.get('message')
    thread = Thread.objects(tid=tid).first()
    data = FormData.objects(thread=thread).order_by('id').first()
    email = data.load['email']
    email_address = current_user.username + '@mail.dyform.co'

    subject = 'Reply To: ' + '[DFNR:' + str(fid) + '-' + str(tid) + ']'

    message = sendgrid.Mail(to=email, subject=subject,
                            text=body, from_email=email_address)
    status, msg = sg.send(message)
    form_data = FormData()
    form_data.thread = thread.to_dbref()
    form_data.load = {"message": body,
                      "from": current_user.username + '@mail.dyform.co'}
    form_data.save()

    return redirect(url_for('forms.data_view', fid=fid, tid=tid))
