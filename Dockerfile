FROM centos/python-38-centos7
USER root

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt ./

RUN yum clean all

# Install python essentials dependencies
RUN yum install gcc openssl-devel  zlib-devel python-devel wget dnf  build-essential  -y

# Install wkhtmltopdf
RUN yum install libXrender libXext fontconfig xorg-x11-font-utils xorg-x11-fonts-Type1 xorg xorg-x11-server-Xvfb libpng-devel -y
RUN yum install -y yum install -y wkhtmltopdf
RUN wget -q https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz -O /tmp/wkhtmltox.tar.xz && \
    tar xvf /tmp/wkhtmltox.tar.xz -C /tmp && \
    cp -rp /tmp/wkhtmltox/* /usr/local && \
    rm -rf /tmp/wkhtmltox*


# installing the libraries
RUN pip3 install -r requirements.txt


# Collect static files (if needed)
# RUN python manage.py collectstatic --noinput

# Expose the Streamlit port
#EXPOSE 8501

# Command to run Streamlit app
#ENTRYPOINT ["streamlit", "run", "hrms_auth/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]



COPY . .

# Collect static files
#RUN python3 manage.py collectstatic --noinput
#RUN python manage.py makemigrations && python manage.py migrate