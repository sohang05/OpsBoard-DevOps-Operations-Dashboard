pipeline {
    agent { label 'OpsBoard' }

    stages {
        stage('Install Docker') {
            steps {
                sh '''
                    if ! command -v docker &> /dev/null; then
                        sudo apt-get update
                        sudo apt-get install -y docker.io
                        sudo systemctl enable --now docker
                        sudo usermod -aG docker ubuntu
                    fi
                    sudo docker --version
                '''
            }
        }

        stage('Build') {
            steps {
                sh '''
                    sudo docker build -t opsboard:latest .
                    sudo docker stop opsboard-app || true
                    sudo docker rm opsboard-app || true
                    sudo docker run -d --name opsboard-app -p 5000:5000 opsboard:latest
                '''
            }
        }
    }
}