properties([pipelineTriggers([githubPush()])])

pipeline {
    agent any

    stages {
        stage('Setup config') {
            steps {
                sh '''#!/bin/bash

                    touch .env
                    echo 'DATABASE_URL=postgresql://ci:123456789@localhost:5432/ci_staging' > .env
                    echo 'JWT_SECRET=zefuihzefizpaefhzoiefhzeiofhze2342ofhizefzoe' > .env
                    echo 'TESTING=true' > .env
                '''
            }
        }
        stage('Setup venv') {
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

                    echo "Activate virtualenv ..."
                    source .venv/bin/activate

                    echo "Running API ..."
                    uvicorn app:app --host 0.0.0.0 --port 8080
                '''
            }
        }
    }
    post {
        always {
            sh '''#!/bin/bash
                rm .env
                rm -Rf .venv
            '''   
        }
    }
}