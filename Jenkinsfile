pipeline {

    agent any

    environment {

        IMAGE_NAME = "vishalpatillll/flask-app"

        DOCKER_CREDS = credentials('dockerhub-creds')
    }

    stages {

        stage('Checkout') {

            steps {

                git branch: 'main',
                credentialsId: 'github-creds',
                url: 'https://github.com/vishalforaws333-debug/gitops-jenkins-argocd.git'
            }
        }

        stage('Build Docker Image') {

            steps {

                sh '''
                docker build -t $IMAGE_NAME:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Push Docker Image') {

            steps {

                sh '''
                echo ${DOCKER_CREDS_PSW} | docker login \
                -u ${DOCKER_CREDS_USR} \
                --password-stdin

                docker push $IMAGE_NAME:${BUILD_NUMBER}
                '''
            }
        }

        stage('Update Deployment YAML') {

            steps {

                sh '''
                sed -i "s|image:.*|image: ${IMAGE_NAME}:${BUILD_NUMBER}|g" k8s/deployment.yaml
                '''
            }
        }

        stage('Commit and Push Changes') {

            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-creds',
                        usernameVariable: 'GIT_USER',
                        passwordVariable: 'GIT_TOKEN'
                    )
                ]) {

                    sh '''
                    git config user.email "jenkins@local"
                    git config user.name "jenkins"

                    git add k8s/deployment.yaml

                    git commit -m "Updated image tag ${BUILD_NUMBER}" || true

                    git push https://${GIT_USER}:${GIT_TOKEN}@github.com/vishalforaws333-debug/gitops-jenkins-argocd.git HEAD:main
                    '''
                }
            }
        }
    }
}
