FROM quartorz/manim-japanese:v1.0.0

ARG SARASA_GOTHIC_VERSION=1.0.25

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends p7zip-full \
    && wget https://github.com/be5invis/Sarasa-Gothic/releases/download/v${SARASA_GOTHIC_VERSION}/Sarasa-TTC-${SARASA_GOTHIC_VERSION}.7z \
    && 7z x Sarasa-TTC-${SARASA_GOTHIC_VERSION}.7z \
    && mv *.ttc /usr/local/share/fonts \
    && rm Sarasa-TTC-${SARASA_GOTHIC_VERSION}.7z \
    && fc-cache -r

USER ${USER}
