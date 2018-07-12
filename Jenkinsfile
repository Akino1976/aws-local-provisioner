#!groovy

IMAGE_NAME = 'aws-local-provisioner'
REPO_NAME = 'aws-local-provisioner'

SLACK_CREDENTIALS = 'slack-trendsetters'
SLACK_CHANNEL_CI = '#sto-sos-ci'
SLACK_CHANNEL_DEPLOY = '#sto-sos'

TARGET_REGIONS = ['eu-west-1']

utils = new com.bambora.jenkins.pipeline.Utils()


def slack(String msg, String channel = '', String color = null) {
    withCredentials([
        [
            $class: 'UsernamePasswordMultiBinding',
            credentialsId: SLACK_CREDENTIALS,
            usernameVariable: 'USERNAME',
            passwordVariable: 'PASSWORD'
        ]
    ]) {
        slackSend(message: msg, color: color, token: "${env.PASSWORD}", channel: channel)
    }
}


def notify_start(message) {
    slack("${REPO_NAME} (${env.BRANCH_NAME}): ${message}. Result at ${env.BUILD_URL}", SLACK_CHANNEL_CI, 'info')
}


def notify_success(message) {
    slack("${REPO_NAME} (${env.BRANCH_NAME}): ${message}. Result at ${env.BUILD_URL}", SLACK_CHANNEL_CI, 'good')
}


def notify_failure(message) {
    slack("${REPO_NAME} (${env.BRANCH_NAME}): ${message}. Result at ${env.BUILD_URL}", SLACK_CHANNEL_CI, 'danger')
}


def build(version) {
    stage('build') {
        was_successful = utils.shell('make build-provisioner')

        if (!was_successful) {
            notify_failure("Failed to build ${IMAGE_NAME}:${version}")

            error 'Build stage failed'
        }
    }
}


def push(version) {
    stage('push') {
        try {
            utils.ecrLogin(TARGET_REGIONS)

            utils.ecrCreateRepo("${IMAGE_NAME}", TARGET_REGIONS)
            utils.ecrSetRepoPolicy("${IMAGE_NAME}", TARGET_REGIONS)
            utils.tagAndPushDockerImage("${IMAGE_NAME}:${version}", TARGET_REGIONS)

            if (env.BRANCH_NAME == 'master') {
                utils.tagAndPushDockerImage("${IMAGE_NAME}:latest", TARGET_REGIONS)
            }
        } catch (Exception err) {
            notify_failure("Failed to push ${IMAGE_NAME}:${version}")

            error err
        }
    }
}


node('!master && docker-concurrent') {
    checkout scm

    try {
        assert VERSION
    } catch (Exception _) {
        VERSION = sh(returnStdout: true, script: "make date").trim()
    }

    if (env.BRANCH_NAME != 'master') {
        VERSION = "${VERSION}-${env.BRANCH_NAME}"
    }

    env.VERSION = VERSION

    echo "VERSION is ${VERSION}"

    notify_start("Building and pushing ${IMAGE_NAME}:${VERSION}")

    build(VERSION)
    push(VERSION)

    notify_success("Successfully built and pushed ${IMAGE_NAME}:${VERSION}")
}
