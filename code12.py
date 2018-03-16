import urllib2
#from PIL import Image
import pyDes
#import PIL.Image
import base64
import hashlib
from flask import Flask, render_template, request

# from Crypto.Cipher import AES
import swiftclient
import keystoneclient
import os

# from simple_aes_cipher import cipher

auth_url= 'https://identity.open.softlayer.com'+ '/v3'
projectId= '92e6d2e713fb45cd9dda22d53f963fa8'
region= 'dallas'
userId= 'f37a115fd99d49b6b0617851a89a38be'
password= 'yg~AGMGvLN&TY25M'
container_name = 'vir', 'Virti'
conn = swiftclient.Connection(key=password,
                              authurl=auth_url,
                              auth_version='3',
                              os_options={"project_id": projectId,
                                          "user_id": userId,
                                          "region_name": region})
dpath = '/home/vinayak/Downloads/IBM-Bluemix-Cloud--File-encryption-Da-storage-master/download'
folder = '/home/vinayak/Downloads/IBM-Bluemix-Cloud--File-encryption-Da-storage-master/upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'jpg', 'jpeg', 'gif'])

k = pyDes.des("DESCRYPT", pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = folder

dic={}
@app.route('/', methods=['POST', 'GET'])
def main_page():
    res = ""
    if request.method == 'POST':
        if request.form['submit'] == 'Upload':
            f = request.files['file_upload']
            key = request.form['key']
            print 'a'
            pushobj(f.filename)

        elif request.form['submit'] == 'Download':
            f1 = request.form['file_download']
            dkey = request.form['dkey']
            print f1
            pullobj(f1)

        elif request.form['submit'] == 'List':
            print 'list'
            res = list()

        elif request.form['submit'] == 'Listlocal':
            print 'list'

            res = listlocal()

        elif request.form['submit'] == 'Remove':
            size = request.form['fsize']
            remove(size)

    return render_template('index1.html', res=res)


def pushobj(filename):
    # fname, ext = os.path.splitext(filename)
    # if ext == ".txt":
    fl = open('/home/vinayak/Downloads/IBM-Bluemix-Cloud--File-encryption-Data-storage-master/upload' + "/" + filename, "rb")
    data = fl.read()
    #  content=encrypt_val(data,key)
    print 'data'+ data
    # contents = cipher.encrypt(data,ukey)
    no = checksum(filename)
    print'hi'+ no
    text = data+'$$$$$$$$$'+no
    contents = k.encrypt(text)
    dic[filename]=no
    print 'hello'+ dic[filename]
    # print contents
    fname, ext = os.path.splitext(filename)
    print fname
    if ext == ".txt":
        conn.put_object('vir', filename, contents, content_type='text/plain')
    else:
        # imagefile = Image.open('C:/Users/srinivas venkatesh/Documents/cloud computing/assg1/files' + "/" + filename)
        # contents = open('C:/Users/srinivas venkatesh/Documents/cloud computing/assg1/files' + "/" + filename, 'rb').read()
        # contents = base64.b64encode('C:/Users/srinivas venkatesh/Documents/cloud computing/assg1/files/' + filename)
        #This has to be reviewed and removed
        conn.put_object('Virti', filename, contents, content_type='text/plain')
    print filename
    fl.close()

    #os.remove('C:/Users/srinivas venkatesh/Documents/cloud computing/assg1/files' + "/" + filename)


def listlocal():
    dirs = os.listdir('/home/vinayak/Downloads/IBM-Bluemix-Cloud--File-encryption-Data-storage-master/upload')
    list = []
    for f in dirs:
        list.append(f);
        print f
    return list

def checksum(filename):
    md5 = hashlib.md5()
    with open('/home/vinayak/Downloads/IBM-Bluemix-Cloud--File-encryption-Data-storage-master/upload' + "/" +filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
            print 'function'+md5.hexdigest()
    return md5.hexdigest()
    # do something


# def encrypt_val(ftext,ukey):
# ftext = pad(ftext)
#  iv = Random.new().read(AES.block_size)
# cipher = AES.new(ukey, AES.MODE_CBC, iv)
# return base64.b64encode(iv + cipher.encrypt(ftext))


# def decrypt(encryp, ukey):
#   enc = base64.b64decode(encryp)
#  iv = enc[:16]
#  cipher = AES.new(ukey, AES.MODE_CBC, iv)
#  return unpad(cipher.decrypt(enc[16:]))


def pullobj(filename):
    fname, ext = os.path.splitext(filename)
    # for files in conn.get_container(container_name)[1]:
    # if filename == files['name']:
    print "Fname  ",fname,"  extn  ",ext
    for container in conn.get_account()[1]:
        #print "Container ",container
        for data1 in conn.get_container(container['name'])[1]:
            print filename
            #print data1['name']
            if filename == data1['name']:
                print "in if"
                try:
                    fobj = conn.get_object(container['name'], filename)
                    print fobj
                    # contents = k.decrypt(dfile)
                    # print 'a'
                    # if ext == '.txt':
                    with open("/home/vinayak/Downloads/"+ filename, 'wb') as fw:
                        data = fobj[1]
                        # d = cipher.decrypt(data,dkey)

                        d = k.decrypt(data)
                        data,number = d.split('$$$$$$$$$')
                        print 'data'+data
                        print 'no'+number
                        print dic
                        if number in dic[filename] :
                            print 'correct file'
                            fw.write(data)
                            fw.close()
                        else:
                           print 'incorrect file'


                        # print d
                        #fw.write(data)
                        # fw.write(fobj[1])
                        #fw.close()
                        #  Decrypt the file
                        # with open(filename, 'rb') as fw1:
                        #  d = fw1.read()
                        #   data = k.decrypt(d)
                        #   print data
                        #   fw1.close()
                        # Write the decrypted content to /downloads folder
                        # with open(dpath + filename, 'wb') as ffile:
                        #    ffile.write(str(data))
                        #    ffile.close()
                        #    print 'done'
                        # else:
                        # with open(dpath +filename, 'wb') as fw:
                        #    fw.write(fobj[1])
                        #    fw.decode('base64')
                        #   fw.close()
                except urllib2.HTTPError as err:
                    if err.code == 404:
                        continue


def delete(filename):
    for container in conn.get_account()[1]:
        conn.delete_object(container['name'], filename)


def remove(size):
    print "remove function"
    for container in conn.get_account()[1]:
        for data in conn.get_container(container['name'])[1]:
            print data['bytes']
            if int(data['bytes']) > int(size):
                print data['bytes'], size
                conn.delete_object(container['name'], data['name'])


def list():
    print ("nObject List:")
    list = ""
    for container in conn.get_account()[1]:
        for data in conn.get_container(container['name'])[1]:
            print container['name']
            print 'object: {0}t size: {1}t date: {2}'.format(data['name'], data['bytes'], data['last_modified'])
            list+=('\r\nobject: {0}t size: {1}t date: {2}\r\n'.format(data['name'], data['bytes'], data['last_modified']))
            # @app.route('/upload')
            # def upload():
            #  return render_template('upload.html')
    return list

@app.route('/Exit')
def exitf():
    funct = request.environ.get('werkzeug.server.shutdown')
    print 'shut'
    if funct is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    funct()
    return 'the application ended'


port = int(os.getenv('VCAP_APP_PORT', '5000'))
if __name__ == '__main__':
    app.run(debug=True, port=port)
    # host='0.0.0.0'
