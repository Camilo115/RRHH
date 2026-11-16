package cl.proyecto.recursos_humanos_autenticacion_service.security;

import java.util.Date;
import javax.crypto.SecretKey;
import org.springframework.stereotype.Service;
import io.jsonwebtoken.Jwts;

@Service 
public class JwtService {
    
    private final SecretKey key;

    public JwtService(SecretKey key) {
        this.key = key;
    }

    public String generarToken(String username) {
        return Jwts.builder()
                .subject(username)
                .issuedAt(new Date())
                .expiration(new Date(
                    System.currentTimeMillis() + 3600000
                ))
                .signWith(key)
                .compact();
    }
}
