package com.example.clients;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;

@Service
public class CommandeConsumer {

    private final Map<Integer, Integer> commandesParClient = new HashMap<>();

    @KafkaListener(
            topics = "commandes-creees",
            groupId = "clients-group"
    )
    public void recevoirCommande(Commande commande) {

        int clientId = commande.getClient_id();

        commandesParClient.put(
                clientId,
                commandesParClient.getOrDefault(clientId, 0) + 1
        );

        System.out.println("================================");
        System.out.println("Nouvelle commande reçue !");
        System.out.println("Commande : " + commande.getCommande_id());
        System.out.println("Client   : " + clientId);
        System.out.println("Produit  : " + commande.getProduit());
        System.out.println("Montant  : " + commande.getMontant());
        System.out.println(
                "Nombre de commandes du client "
                + clientId
                + " : "
                + commandesParClient.get(clientId)
        );
        System.out.println("================================");
    }
}
