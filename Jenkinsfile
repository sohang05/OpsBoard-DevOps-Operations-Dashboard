pipeline {
    agent { label 'OpsBoard' }

    environment {
        DOCKER_IMAGE = 'sohang05/opsboard'
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
    }

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
                    sudo docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} -t ${DOCKER_IMAGE}:latest .
                '''
            }
        }
        stage('Push to DockerHub'){
            steps {
                withCredentials([usernamePassword(
                credentailsId: 'dockerHubCred',
                usernameVariable: 'DOCKER_USER',
                passwordVariable: 'DOCKER_PASS'
                )]){
                    sh '''
                    echo "$DOCKER_PASS" | sudo docker login -u "$DOCKER_USER"
                    sudo docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                    sudo docker push ${DOCKER_IMAGE}:latest
                    sudo docker logout
                    '''
                }
            }
        }
        stage('Deploy Container'){
            steps {
                sh '''
                sudo docker stop opsboard-app || true
                sudo docker rm opsboard-app || true
                sudo docker run -d --name opsboard-app -p 5000:5000 opsboard:latest
                '''
            }
        }
    }
}