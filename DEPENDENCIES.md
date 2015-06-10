Probably most of these will be necessary

python-gi
python-opengl or pyopengl
python-gi-cairo
gir1.2-gtksource-3.0 # source buffer
gir1.2-gstreamer-0.10 # sound

OpenGLContext
http://pyopengl.sourceforge.net/documentation/installation.html
	virtualenv oglc-env
	source oglc-env/bin/activate
	pip install PyOpenGL PyOpenGL_accelerate "PyVRML97==2.3.0a4" simpleparse numpy "OpenGLContext==2.2.0a3" pydispatcher pillow

pygobject
https://python-gtk-3-tutorial.readthedocs.org/en/latest/install.html

pygobject2-devel

In Fedora 22
sudo dnf install PyOpenGL
sudo dnf install libX11-devel
