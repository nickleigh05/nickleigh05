#!/usr/bin/env node
const c = {
  reset: "\x1b[0m",
  green: "\x1b[32m",
  dim: "\x1b[2m",
  bold: "\x1b[1m",
  cyan: "\x1b[36m",
};

const banner = `
${c.green}${c.bold}    _   ___      __      __         _       __
   / | / (_)____/ /__   / /   ___  (_)___ _/ /_
  /  |/ / / ___/ //_/  / /   / _ \\/ / __ \`/ __ \\
 / /|  / / /__/ ,<    / /___/  __/ / /_/ / / / /
/_/ |_/_/\\___/_/|_|  /_____/\\___/_/\\__, /_/ /_/
                                  /____/${c.reset}
`;

const lines = [
  ["$", "whoami"],
  [" ", "nick — ASU CS · cloud + AI/ML"],
  ["$", "cat interests.txt"],
  [" ", "cloud infra, AI/ML, RL, neural nets from scratch"],
  ["$", "ls projects/"],
  [" ", "cloud-collar  MMA-Machine  NNFS  nicksnexus"],
  ["$", "open"],
  [" ", "linkedin.com/in/-nicholas-leigh"],
  [" ", "nickleigh05.github.io/nicksnexus"],
];

async function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function main() {
  console.log(banner);
  for (const [prompt, text] of lines) {
    const prefix =
      prompt === "$" ? `${c.green}$ ${c.reset}` : `${c.dim}  ${c.reset}`;
    process.stdout.write(prefix);
    for (const ch of text) {
      process.stdout.write(ch);
      await sleep(12);
    }
    process.stdout.write("\n");
    await sleep(120);
  }
  console.log(`\n${c.cyan}thanks for stopping by.${c.reset}\n`);
}

main();
