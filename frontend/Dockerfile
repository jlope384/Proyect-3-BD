# Usa la imagen oficial de Node
FROM node:18-alpine

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de dependencias
COPY package.json yarn.lock* ./

# Instala dependencias
RUN npm install

# Copia el resto de los archivos
COPY . .

# Construye la aplicación
RUN npm run build

# Expone el puerto
EXPOSE 5173

# Comando para iniciar la aplicación
CMD ["npm", "run", "dev"]