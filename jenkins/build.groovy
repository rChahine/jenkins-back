pipeline {
    agent any
    stages {
        stage('Create venv') {
            steps {
                powershell '''
                    python -m venv .venv
                '''
            }
        }
        stage('Setup .env') {
            steps {
                    powershell '''
                        Out-File -FilePath .env

                        echo DATABASE_URL=postgresql://u3ggi38lxczfan4hmvqp:0ociuSjr4TkmPuf510CG@b9urnsqkuw5cfwy1io7c-postgresql.services.clever-cloud.com:5432/b9urnsqkuw5cfwy1io7c >> .env
                        echo SECRET_KEY=zefuihzefizpaefhzoiefhzeiofhze2342ofhizefzoe >> .env
                        echo TESTING=true >> .env
                    '''
            }
        }
        stage('Setup virtual env') {
            steps {
                powershell '''

                    echo "Running virtualenv ..."
                    .venv/Scripts/activate

                    echo "Install dependencies ..."
                    pip install -r requirements.txt --no-cache-dir
                '''
            }
        }
        
        stage('Migrate database') {
            steps {
                powershell '''

                    echo "Activate virtualenv ..."
                    .venv/Scripts/activate

                    echo "Migrating database ..."
                    alembic upgrade head
                '''
            }
        }
        stage('Run application') {
            steps {
                powershell '''

                    echo "Activate virtualenv ..."
                    .venv/Scripts/activate

                    echo "Running API ..."
                    uvicorn app:app --host 0.0.0.0 --port 8080
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
