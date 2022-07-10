FROM python


RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc


COPY Pipfile .
COPY Pipfile.lock .
COPY api.py .

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --system --deploy --ignore-pipfile

#RUN pipenv shell
RUN python -m spacy download en

CMD ["python", "api.py"]