function timer(seconds) {
    return new Promise(resolve => {
      setTimeout(() => {
        resolve('resolved');
      }, seconds * 1000);
    });
  }

const CR = '\r';

async function spin(msg, computation) {
    out = process.stdout;
    for (const char of '⠇⠋⠙⠸⠴⠦') {
        await timer(.1);
        status = CR + char + ' ' + msg;
        out.write(status);
    }
    blanks = ' '.repeat(status.length);
    out.write(CR + blanks + CR);
}


async function slowFunction() {
    await timer(3);
    return 42;
}

async function supervisor() {
    const computation = new Promise((resolve, reject) => {});
    const spinner = spin('thinking!', computation);
    console.log('spinner object:', spinner);
    const result = await slowFunction();
    return result;
}

async function main() {
    result = await supervisor();
    console.log('Answer:', result);
}

main();
