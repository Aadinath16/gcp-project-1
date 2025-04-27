pipeline {
    agent any

    environment {
        PROJECT_ID = 'resonant-kayak-321707'      // Replace with your GCP project ID
        PROJECT_NAME = 'gcp-project-1'           // Your app's name
        APP_NAME = 'python-app'
       // CLUSTER_NAME = 'your-gke-cluster-name'   // Replace with your GKE cluster name
       // CLUSTER_ZONE = 'your-cluster-zone'       // Replace with your GKE zone, like us-central1-a
       //  IMAGE_TAG = "us-central1-docker.pkg.dev/${PROJECT_ID}/${PROJECT_NAME}/${APP_NAME}:${BUILD_NUMBER}"
       // IMAGE_TAG = "us-central1-docker.pkg.dev/resonant-kayak-321707/gcp-project-1/python-app:${BUILD_NUMBER}"
        GITHUB_TOKEN = credentials('github-token')
    }

    stages {
    /*    stage('Checkout Code') {
            steps {
                checkout scm
                sh '''
                    git fetch --all
                    git checkout ${GIT_BRANCH#origin/}
                '''
            }
        } */

        stage('Checkout Code') {
            steps {
                script {
                    // Get the branch name without the prefix
                    def branch = sh(script: 'git rev-parse --abbrev-ref HEAD', returnStdout: true).trim()
                    echo "Branch name: ${branch}"

                    // Checkout the branch explicitly
                    sh "git checkout ${branch}"
                }
            }
        }

        stage('Install Semantic Release') {
            steps {
                sh 'npm install semantic-release @semantic-release/exec @semantic-release/changelog @semantic-release/git'
            }
        }

        stage('Run Semantic Release') {   
            steps {
                echo "Branch name: ${branch}"
                sh 'npx semantic-release --debug'
            }
        }

        stage('Load Version and Build Docker Image') {
            steps {
                script {
                    env.RELEASE_VERSION = readFile('version.txt').trim()
                    env.IMAGE_TAG = "us-central1-docker.pkg.dev/${env.PROJECT_ID}/${env.PROJECT_NAME}/${env.APP_NAME}:${env.RELEASE_VERSION}"
                }
                sh '''
                echo "Building Docker Image with tag $IMAGE_TAG..."
                cd src/
                docker build -t $IMAGE_TAG .
                '''
            }
        }
        stage('Push Docker Image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GCP_KEY')]) {
                    sh '''
                    echo "Authenticating with GCP..."
                    gcloud auth activate-service-account --key-file=$GCP_KEY
                    gcloud auth configure-docker us-central1-docker.pkg.dev

                    echo "Pushing Docker Image to Google Container Registry..."
                    docker push $IMAGE_TAG
                    '''
                }
            }
        }
    }
    post {
        success {
            echo "✅ Deployment Successful!"
        }
        failure {
            echo "❌ Deployment Failed!"
        }
        always {
            cleanWs()
        }
    }
}

