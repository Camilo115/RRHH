package cl.proyecto.recursos_humanos_autenticacion_service.controller;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import cl.proyecto.recursos_humanos_autenticacion_service.repository.UsuarioRepository;

@RestController
@RequestMapping ("/usuario")
public class UsuarioController {
    
    private UsuarioRepository usuarioRespository;

    public UsuarioController(UsuarioRepository usuarioRespository) {
        this.usuarioRespository = usuarioRespository;
    }

}
