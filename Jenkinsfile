pipeline {
  agent {
    kubernetes {
      label 'dbmigration-builder'
      yaml """
apiVersion: v1
kind: Pod
spec:
  containers:  # list of containers that you want present for your build, you can define a default container in the Jenkinsfile
    - name: docker
      image: docker:18.06.1
      command: ["tail", "-f", "/dev/null"]
      imagePullPolicy: Always
      volumeMounts:
        - name: docker
          mountPath: /var/run/docker.sock # We use the k8s host docker engine
  volumes:
    - name: docker
      hostPath:
        path: /var/run/docker.sock
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
