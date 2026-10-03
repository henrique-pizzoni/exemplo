pipeline {
    // "agent any": roda em qualquer maquina disponivel do Jenkins.
    // No nosso caso, o proprio container do Jenkins.
    agent any

    stages {


        //  BUILD: prepara o projeto
      
        stage('Build') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements.txt
                    python -c "import main"
                '''
            }
        }

        //  TEST: roda os testes automatizados

        stage('Test') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest --junitxml=reports/junit.xml
                '''
            }
            post {
                always {
                    junit 'reports/junit.xml'
                }
            }
        }

        //  DEPLOY: publica a nova versao em producao

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                withCredentials([string(credentialsId: 'render-deploy-hook', variable: 'DEPLOY_HOOK')]) {
                    sh 'curl -fsS -X POST "$DEPLOY_HOOK"'
                }
                echo 'Deploy disparado! Acompanhe no painel do Render.'
            }
        }
    }

    // Roda no final de tudo, deu certo ou nao
    post {
        success { echo 'Pipeline VERDE: tudo certo.' }
        failure { echo 'Pipeline VERMELHA: pare tudo e conserte antes de seguir!' }
    }
}
