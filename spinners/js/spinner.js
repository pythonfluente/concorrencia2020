function timer(seconds) {
    return new Promise((resolve) => setTimeout(resolve, seconds * 1000));
}

function spin(msg) {
    const out = process.stdout;
    const CR = '\r';
    let status;

    function *genStatuses() {
        while (true) {
            for (const char of '⠇⠋⠙⠸⠴⠦') {
                status = CR + char + ' ' + msg;
                yield status;
            }
        }
    }

    const statuses = genStatuses()
    new Promise(async () => {
        await timer(0.1);
        for (const status of statuses) {
            out.write(status);
            await timer(0.1);
        }
    })

    const cancel = () => {
        statuses.return()
        const blanks = ' '.repeat(status.length);
        out.write(CR + blanks + CR);
    };
    return { cancel };
}

async function slowFunction() {
    await timer(3);
    return 42;
}

async function supervisor() {
    const spinner = spin('thinking!');
    console.log('spinner object:', spinner);
    const result = await slowFunction();
    spinner.cancel();
    return result;
}

async function main() {
    const result = await supervisor();
    console.log('Answer:', result);
}

main();
