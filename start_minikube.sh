#!/bin/bash

echo "🧹 Suppression des anciennes configurations Minikube..."
minikube delete --all --purge

echo "🚀 Démarrage de Minikube avec Docker..."
minikube start --driver=docker --memory=4096 --cpus=2

echo "✅ Activation de l'ingress NGINX..."
minikube addons enable ingress

echo "📦 Chargement des images Docker locales dans Minikube..."
minikube image load devops_meeting_reservation-user_service:latest
minikube image load devops_meeting_reservation-salle_service:latest
minikube image load devops_meeting_reservation-reservation_service:latest

echo "📁 Déploiement des fichiers Kubernetes..."
kubectl apply -f k8s/

echo ""
echo "🌐 Lance maintenant 'minikube tunnel' dans un autre terminal"
echo "Puis accède à ton application via http://meeting.local"
