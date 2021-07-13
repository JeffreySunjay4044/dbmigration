pipeline {
  agent {
    kubernetes {
      label 'dbmigration-builder'
      yaml """

apiVersion: v1
kind: Pod
spec:
  containers:
  - name: jenkins-builder
    image: 'jenkins/inbound-agent:4.7-1'
    args: ['\$(JENKINS_SECRET)', '\$(JENKINS_NAME)']

"""
    }
  }
  stages {
    stage('docker login') {
        steps {
          container('jenkins-builder') {
              sh 'docker login -u sunjayjeffrish --password !gP5tCAPbJYz=G_'
          }
        }
      }
    stage('build') {
      steps {
        container('jenkins-builder') {
          dir("costAnalyser") {
            sh "docker build . -f Dockerfile -t sunjayjeffrish/dbmigration:$GIT_COMMIT"
          }
        }
      }
    }
    stage('push') {
      steps {
        container('jenkins-builder') {
          sh "docker push"
        }
      }
    }
  }
}