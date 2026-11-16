package cl.proyecto.recursos_humanos_autenticacion_service.controller;

import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseCookie;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import cl.proyecto.recursos_humanos_autenticacion_service.dto.LoginRequest;
import cl.proyecto.recursos_humanos_autenticacion_service.model.Usuario;
import cl.proyecto.recursos_humanos_autenticacion_service.repository.UsuarioRepository;
import cl.proyecto.recursos_humanos_autenticacion_service.service.JwtService;

@RestController
@RequestMapping("/auth")
public class AuthController {

    private final JwtService jwtService;
    private final UsuarioRepository usuarioRepository;

    public AuthController(JwtService jwtService, UsuarioRepository usuarioRepository) {
        this.jwtService = jwtService;
        this.usuarioRepository = usuarioRepository;
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest request) {

        Usuario usuario = usuarioRepository.findByCorreo(request.correo()).orElse(null);

        if (usuario == null || !usuario.getContrasena().equals(request.password())) {
            return ResponseEntity.status(401).body("Correo o contraseña incorrecto");
        }

        String token = jwtService.generarToken(usuario.getCorreo());

        ResponseCookie cookie = ResponseCookie.from("sesion", token)
                .httpOnly(true)
                .secure(false) // Solo para desarrollo en localhost
                .path("/")
                .maxAge(3600)
                .sameSite("Lax")
                .build();

        return ResponseEntity.ok()
                .header(HttpHeaders.SET_COOKIE, cookie.toString())
                .body("Inicio de sesión exitoso");
    }
}
