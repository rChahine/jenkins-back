pipeline {
    agent any

    stages {
        stage('Create venv') {
            steps {
                sh '''#!/bin/bash
                    python3.9 -m venv .venv
                '''
            }
        }
        stage('Setup .env') {
            steps {
                sh '''#!/bin/bash

                    touch .env
                    echo '
                        DATABASE_URL=postgresql://ci:123456789@localhost:5432/ci_staging
                        JWT_SECRET=zefuihzefizpaefhzoiefhzeiofhze2342ofhizefzoe
                        TESTING=true
                    ' > .env
                '''
            }
        }
        stage('Setup virtual env') {
            steps {
                sh '''#!/bin/bash

                    echo "Running virtualenv ..."
                    source .venv/bin/activate

                    echo "Install dependencies ..."
                    pip install -r requirements.txt --no-cache-dir
                '''
            }
        }
        stage('Setup database') {
            steps {
                sh '''#!/bin/bash

                    echo "Clear Database ..."
                    sudo -u postgres psql -c "DROP DATABASE IF EXISTS ci_staging;"
                    
                    echo "Setup new Database ..."
                    sudo -u postgres psql -c "CREATE DATABASE ci_staging;"
                '''
            }
        }
        stage('Migrate database') {
            steps {
                sh '''#!/bin/bash

                    echo "Activate virtualenv ..."
                    source .venv/bin/activate

                    echo "Migrating database ..."
                    alembic upgrade head
                '''
            }
        }
        stage('test') {
            steps {
                sh '''#!/bin/bash
                    echo "Activate virtualenv ..."
                    source .venv/bin/activate

                    echo "Running tests ..."
                    pytest
                '''
            }
        }
    }

    post {
        always {
            echo 'Delete directory'
            deleteDir()
        }
    }
}