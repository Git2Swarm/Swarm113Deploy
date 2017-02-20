node ('docker-build') {
  
  stage ('Initialze Build') {
    checkout scm
    sh "docker login -u ${env.DOCKER_HUB_USER} -p ${env.DOCKER_HUB_PASSWORD}"
  }
  mergeArg = ""
  composeInput = "${env.APPS_COMPOSE}"
  composeList = composeInput.tokenize(';')
  
  for ( url in composeList ) {
    items = url.split("/blob/master/")
    
    // Extract the git URL and project name
    def gitUrl = "${items[0]}.git"
    def projectName = items[0].tokenize('/')[3]
      
    // Extract the compose file with path
    def composePath = items[1]
    
    mergeArg = "$mergeArg /data/$projectName/$composePath"
    stage ("Project $projectName") {
      dir ("$projectName") {
        git url: "$gitUrl"
        sh "git submodule update --init"
        sh "git submodule update --force"
        sh "docker-compose -f $composePath build --pull "
        sh "docker-compose -f $composePath push"
      }
    }  
  }    
  
  stage ("Merge Compose files") {
    sh "docker run --rm -v `pwd`:/data mikeagileclouds/composemerger --output /data/${env.JOB_NAME}.yml ${mergeArg}"
    sh "curl -k -u ${env.ARTIFACTORY_USER}:${env.ARTIFACTORY_PASSWORD} -X PUT ${env.ARTIFACTORY_URL}/${env.JOB_NAME}.yml -T ${env.JOB_NAME}.yml"
  }
}

node ('swarm-deploy') {
  stage ('Initialize Deployment') {
    checkout scm
  }

  stage ('Download Stack Compose') {
    sh "curl -k -u ${env.ARTIFACTORY_USER}:${env.ARTIFACTORY_PASSWORD}  ${env.ARTIFACTORY_URL}/${env.JOB_NAME}.yml -o ${env.JOB_NAME}.yml"
  }
    
  stage ('Deploy Docker App Bundle') {
    sh "docker stack deploy -c ${env.JOB_NAME}.yml ${env.JOB_NAME}" // deploy create as well as update stack - ?Does note seem to be working?
  }

  stage ('Publish Swarm Node and Service details') {
    sh "docker node ls"
    sh "docker stack ls"
    sh "docker service ls"
  }
}
