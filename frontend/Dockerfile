FROM node:18-alpine
WORKDIR /app

# Copiamos solo package.json y lockfile
COPY package.json yarn.lock* ./

# Instalamos sin generar node_modules en el host
RUN npm install

# Copiamos el resto del código (node_modules queda fuera por .dockerignore)
COPY . .

# Construimos la app
RUN npm run build

EXPOSE 5173

# En CRA el comando de dev es "npm start"
CMD ["npm", "start"]
