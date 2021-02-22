pipeline {
    agent any

    stages {
        stage('prepare') {
            steps {
                sh '''#!/bin/bash
                    rm .env
                    touch .env
                    echo '
                        DATABASE_URL=postgresql://ci:123456789@localhost:5432/ci_test
                        JWT_SECRET=zefuihzefizpaefhzoiefhzeiofhze2342ofhizefzoe
                        TESTING=true
                    ' > .env
                '''
            }
        }
        stage('Setup venv') {
            steps {
                sh '''#!/bin/bash

                    echo "Running virtualenv ..."
                    source .venv/bin/activate

                    echo "Install dependencies ..."
                    pip install -r requirements.txt
                '''
            }
        }
        stage('test') {
            steps {
                sh '''#!/bin/bash
                   echo "Running tests ..."
                   pytest
                '''
            }
        }
    }
}