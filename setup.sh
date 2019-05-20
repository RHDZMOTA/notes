#!/usr/bin/env bash

echo "Creating files..."
mkdir -p ./.notes/pdf
cp ./.env.example ./.env
cp ./.notes/src/resources/references.bib.example ./.notes/src/resources/references.bib


echo "Installing dependencies..."

# Install git & jq
sudo apt install -y git jq

# Install python and venv
sudo apt install -y python3.7
python3.7 -m pip install virtualenv
python3.7 -m virtualenv --python=python3.7 venv
./venv/bin/python -m pip install -r requirements.txt

# Install java 8
sudo apt install -y openjdk-8-jdk

# Install pandoc
sudo apt install -y pandoc pandoc-citeproc

# Install R & Dependencies
sudo apt install -y r-base
sudo apt install -y libcurl4-openssl-dev libssl-dev libxml2-dev r-cran-xml
printf "install.packages(c('rmarkdown', 'tinytex', 'reticulate', 'bookdown'), repos = 'http://cran.us.r-project.org')" | sudo R --vanilla --quiet
printf "install.packages('devtools', dependencies = TRUE, repos = 'http://cran.us.r-project.org')" | R --vanilla --quiet
printf "devtools::install_github('cboettig/knitcitations')" | R --vanilla --quiet

# Install LaTeX
sudo apt install -y texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra


echo "----------------------------------------"
echo "To finalize the installation please run:"
echo "> source venv/bin/activate"
echo "> pip install -r requirements.txt"
echo
echo "Edit the following files with your custom config:"
echo "> vim .env"
echo
echo "[Optional] Download the 'client_secrets.json' file from Google Cloud for the Google Drive integration."
echo
echo "[Optional] Add 'notes' to your shell config as an alias. Copy and paste the result from:  "
echo "> python . alias"
