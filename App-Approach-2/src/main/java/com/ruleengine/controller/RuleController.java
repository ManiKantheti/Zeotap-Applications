//package com.ruleengine.controller;
//
//import com.ruleengine.service.RuleService;
//import com.ruleengine.model.Node;
//import org.springframework.beans.factory.annotation.Autowired;
//import org.springframework.web.bind.annotation.*;
//
//import java.util.List;
//
//@RestController
//@RequestMapping("/api/rules")
//public class RuleController {
//
//    @Autowired
//    private RuleService ruleService;
//
//    @PostMapping("/create")
//    public Node createRule(@RequestBody String ruleString) {
//        return ruleService.createRule(ruleString);
//    }
//
//    @PostMapping("/combine")
//    public Node combineRules(@RequestBody List<String> ruleStrings) {
//        Node[] ruleNodes = ruleStrings.stream().map(ruleService::createRule).toArray(Node[]::new);
//        return ruleService.combineRules(ruleNodes);
//    }
//
//    @PostMapping("/evaluate")
//    public boolean evaluateRule(@RequestBody Node rule, @RequestParam Object userAttributes) {
//        return ruleService.evaluateRule(rule, userAttributes);
//    }
//}
