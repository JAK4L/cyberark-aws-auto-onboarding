pipeline {
  agent {
    node {
      label 'ansible'
    }

  }
  environment {
    BUCKET = 'jenkins-cyberark-aws-auto-onboarding'
    BUCKET_PATH = "${env.BRANCH_NAME}/${env.GIT_COMMIT}"
    TEMPLATE_URL = "https://s3.eu-west-2.amazonaws.com/$BUCKET/$BUCKET_PATH"
    AWS_REGION = 'eu-west-2'
  }
  stages {
    stage('Install virtual environment') {
      steps {
        script {
          sh(script: 'python -m pip install --user virtualenv')
          sh(script: 'python -m virtualenv --no-site-packages .testenv')
          sh(script: 'source ./.testenv/bin/activate')
          sh(script: '.testenv/bin/pip install -r tests/requirements.txt --no-cache-dir')
        }

      }
    }

    stage('Upload templates to S3 bucket') {
      steps {
        s3Upload(bucket: "$BUCKET", file: 'dist', path: "$BUCKET_PATH/")
      }
    }
    stage('Syntax Validation') {
      steps {
        script {
          sh(script: "aws cloudformation validate-template --region $AWS_REGION --template-url $TEMPLATE_URL/aws_auto_onboarding_0.1.1.json", returnStdout: true)
          sh(script: "aws cloudformation validate-template --region $AWS_REGION --template-url $TEMPLATE_URL/aws_auto_onboarding_0.1.1_with_NAT.json", returnStdout: true)
          sh(script: "aws cloudformation validate-template --region $AWS_REGION --template-url $TEMPLATE_URL/NAT-Gateway_0.1.1.json", returnStdout: true)
        }
      }
    }
    stage('cfn-lint') {
      steps {
        script {
          sh(script: ".testenv/bin/cfn-lint dist/aws_auto_onboarding_0.1.1.json", returnStdout: true)
          sh(script: ".testenv/bin/cfn-lint dist/aws_auto_onboarding_0.1.1_with_NAT.json", returnStdout: true)
          sh(script: ".testenv/bin/cfn-lint dist/NAT-Gateway_0.1.1.json", returnStdout: true)
        }
      }
    }
    stage('pytest') {
      steps {
        script {
          sh(script: ".testenv/bin/pytest tests/ --region $AWS_REGION --branch ${env.BRANCH_NAME} --commit-id ${env.GIT_COMMIT} --template-url $TEMPLATE_URL", returnStdout: true)
        }
      }
    }
  }
  post {
    always {
      s3Delete(bucket: "$BUCKET", path: "$BUCKET_PATH/")
    }
  }
}
