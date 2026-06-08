pipeline {


agent any

environment {
    IMAGE_NAME = "vishalpatillll/flask-app"
}

stages {

    stage('Checkout') {
        steps {
            git branch: 'main',
            credentialsId: 'github-creds',
            url: 'https://github.com/vishalforaws333-debug/gitops-jenkins-argocd.git'
        }
    }

    stage('Skip Jenkins Commit') {
        steps {
            script {

                def commitMsg = sh(
                    script: "git log -1 --pretty=%B",
                    returnStdout: true
                ).trim()

                if (commitMsg.contains("Updated image tag")) {
                    error("Skipping Jenkins generated commit")
                }
            }
        }
    }

    stage('Build Docker Image') {
        steps {
            sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
        }
    }

    stage('Push Docker Image') {
        steps {
            withCredentials([
                usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )
            ]) {

                sh """
                echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
                docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                """
            }
        }
    }

    stage('Update Deployment YAML') {
        steps {
            sh """
            sed -i 's|image:.*|image: ${IMAGE_NAME}:${BUILD_NUMBER}|g' k8s/deployment.yaml
            """
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

                sh """
                git config user.email "jenkins@local"
                git config user.name "jenkins"

                git add k8s/deployment.yaml

                git commit -m "Updated image tag ${BUILD_NUMBER}" || true

                git push https://\$GIT_USER:\$GIT_TOKEN@github.com/vishalforaws333-debug/gitops-jenkins-argocd.git HEAD:main
                """
            }
        }
    }
}


}

