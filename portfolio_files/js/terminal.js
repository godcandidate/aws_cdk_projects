class Terminal {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.lines = [];
        this.currentLine = 0;
        this.commands = [
            { cmd: 'whoami', output: 'devops_engineer' },
            { cmd: 'pwd', output: '/home/devops/portfolio' },
            { cmd: 'ls -la projects/', output: 'total 4\ndrwxr-xr-x  2 devops devops 4096 Jan 16 09:19 .\n-rw-r--r--  1 devops devops 2048 Jan 16 09:19 kubernetes-cluster\n-rw-r--r--  1 devops devops 1024 Jan 16 09:19 ci-cd-pipeline\n-rw-r--r--  1 devops devops 3072 Jan 16 09:19 infrastructure-as-code' },
            { cmd: 'docker ps', output: 'CONTAINER ID   IMAGE          COMMAND      CREATED         STATUS         PORTS                    NAMES\nabc123def     nginx:latest   "/docker-..."   2 minutes ago   Up 2 minutes   0.0.0.0:80->80/tcp   web-server\n456789ghi     redis:latest   "redis-ser..."   5 minutes ago   Up 5 minutes   6379/tcp             cache' },
            { cmd: 'kubectl get pods', output: 'NAME                     READY   STATUS    RESTARTS   AGE\nweb-app-7b9bd7b5b-x2jd9   1/1     Running   0          15m\ndb-0                     1/1     Running   0          10m' },
            { cmd: 'terraform plan', output: 'Terraform will perform the following actions:\n\n  + aws_instance.web_server\n      id:                 <computed>\n      ami:                "ami-0c55b159cbfafe1f0"\n      instance_type:      "t2.micro"\n\nPlan: 1 to add, 0 to change, 0 to destroy.' }
        ];
    }

    async typeText(text, element, speed = 50) {
        for (let char of text) {
            element.textContent += char;
            await new Promise(resolve => setTimeout(resolve, speed));
        }
    }

    createLine(content = '', type = 'command') {
        const line = document.createElement('div');
        line.className = `terminal-line ${type}`;
        
        if (type === 'command') {
            const prompt = document.createElement('span');
            prompt.className = 'prompt';
            prompt.textContent = 'devops@portfolio:~$ ';
            line.appendChild(prompt);
        }
        
        const text = document.createElement('span');
        text.className = type;
        text.textContent = content;
        line.appendChild(text);
        
        this.container.appendChild(line);
        return text;
    }

    async simulateCommand() {
        if (this.currentLine >= this.commands.length) {
            this.currentLine = 0;
        }

        const command = this.commands[this.currentLine];
        const commandElement = this.createLine('', 'command');
        await this.typeText(command.cmd, commandElement, 100);
        
        await new Promise(resolve => setTimeout(resolve, 500));
        
        this.createLine(command.output, 'output');
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        this.currentLine++;
        this.simulateCommand();
    }

    start() {
        this.simulateCommand();
    }
}

// Initialize and start the terminal when the page loads
window.addEventListener('load', () => {
    const terminal = new Terminal('terminal');
    terminal.start();
});
