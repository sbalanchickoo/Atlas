FROM jupyter/datascience-notebook:latest
COPY ./xgboost/xgboost-0.90-py2.py3-none-manylinux1_x86_64.whl .
RUN pip install xgboost-0.90-py2.py3-none-manylinux1_x86_64.whl 
COPY ./mlxtend/mlxtend-0.17.0-py2.py3-none-any.whl .
RUN pip install mlxtend-0.17.0-py2.py3-none-any.whl 
COPY ./lightgbm/lightgbm-2.3.0-py2.py3-none-manylinux1_x86_64.whl .
RUN pip install lightgbm-2.3.0-py2.py3-none-manylinux1_x86_64.whl 
# https://files.pythonhosted.org/packages/c1/24/5fe7237b2eca13ee0cfb100bec8c23f4e69ce9df852a64b0493d49dae4e0/xgboost-0.90-py2.py3-none-manylinux1_x86_64.whl
# https://files.pythonhosted.org/packages/52/04/c362f34f666f0ddc7cf593805e64d64fa670ed96fd9302e68549dd48287d/mlxtend-0.17.0-py2.py3-none-any.whl
# https://files.pythonhosted.org/packages/05/ec/756f13b25258e0aa6ec82d98504e01523814f95fc70718407419b8520e1d/lightgbm-2.3.0-py2.py3-none-manylinux1_x86_64.whl