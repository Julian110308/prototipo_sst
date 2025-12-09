from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from .models import Usuario, Visitante
from .serializers import UsuarioSerializer, LoginSerializer, VisitanteSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    # Permisos según acción
    def get_permissions(self):
        if self.action in ['login', 'create', 'register']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    # ---------------------------
    #      LOGIN DE USUARIO
    # ---------------------------
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        usuario = serializer.validated_data['usuario']
        login(request, usuario)

        token, created = Token.objects.get_or_create(user=usuario)

        return Response({
            'token': token.key,
            'usuario': UsuarioSerializer(usuario).data,
            'mensaje': 'Login exitoso.'
        })

    # ---------------------------
    #      LOGOUT DE USUARIO
    # ---------------------------
    @action(detail=False, methods=['post'])
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass

        logout(request)
        return Response({'mensaje': 'Logout exitoso.'})

    # ---------------------------
    #        PERFIL
    # ---------------------------
    @action(detail=False, methods=['get'])
    def perfil(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    # ---------------------------
    #      REGISTRO DE USUARIOS
    # ---------------------------
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        usuario = serializer.save()
        token, created = Token.objects.get_or_create(user=usuario)

        return Response({
            'mensaje': 'Usuario registrado exitosamente.',
            'usuario': UsuarioSerializer(usuario).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


# =====================================================
#              VISITANTES
# =====================================================
class VisitanteViewSet(viewsets.ModelViewSet):
    queryset = Visitante.objects.all()
    serializer_class = VisitanteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(registrado_por=self.request.user)
