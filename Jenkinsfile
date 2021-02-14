properties([pipelineTriggers([githubPush()])])

pipeline {
    agent any

    stages {
        stage('Dependencies') {
            steps {
                sh '''#!/bin/bash

                    echo "Setup virtualenv ..."
                    python3 -m venv .venv

                    echo "Running virtualenv ..."
                    source .venv/bin/activate

                    echo "Install dependencies ..."
                    pip install -r requirements.txt
                '''
            }
        }
        stage('SetupDatabase') {
            steps {
                sh '''#!/bin/bash

                    echo "Clear Database ..."
                    sudo -u postgres psql -c "DROP DATABASE IF EXISTS ci_staging;"
                    
                    echo "Setup new Database ..."
                    sudo -u postgres psql -c "CREATE DATABASE ci_staging;"
                '''
            }
        }
        stage('MigrateDatabase') {
            steps {
                sh '''#!/bin/bash

                    echo "Exporting ENV_MODE var ..."
                    export ENV_MODE=staging
                    
                    echo "Exporting ENV_MODE var ..."
                    export ENV_MODE=staging

                    echo "Activate virtualenv ..."
                    source .venv/bin/activate

                    echo "Migrating database ..."
                    alembic upgrade head
                '''
            }
        }
        stage('RunApi') {
            steps {
                sh '''#!/bin/bash

                    echo "Exporting ENV_MODE var ..."
                    export ENV_MODE=staging
                    export RUNNING_TEST=true
                    
                    echo "Activate virtualenv ..."
                    source .venv/bin/activate

                    echo "Running API ..."
                    uvicorn app:app --host 0.0.0.0 --port 8080
                '''
            }
        }
    }
}